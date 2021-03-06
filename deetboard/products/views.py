from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect
from models import Product, Feature, Link
from serializers import ProductSerializer, FeatureSerializer, LinkSerializer
from rest_framework import generics
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin
from forms import ProductForm, ProductUpdateForm, FeatureForm, FeatureScreenshotForm, FeatureUpdateForm, FeatureScreenshotUpdateForm
from orgs.models import Org
from questions.models import Question
from screenshots.models import Screenshot
from annotations.models import Annotation
from django.contrib.auth.models import Group

from django.http import HttpResponse
from django.views import View
import services

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import assign_perm

from django.http import Http404


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'products/product-create-home.html'

    # Check that user has permission to create products in this org
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        org_pk = self.kwargs['pk']
        org = Org.objects.get(pk=org_pk)
        product_create_perm = user.has_perm('orgs.create_prod', org)
        if(not product_create_perm):
            return redirect('/home/')
        return super(ProductCreateView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Use this to add extra context (the user)."""
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        user = self.request.user
        org_pk = self.kwargs['pk']
        org = Org.objects.get(pk=org_pk)
        user_orgs = user.orgs.all()
        products = org.products.all()
        context['user'] = user
        context['org'] = org
        context['user_orgs'] = user_orgs
        context['org_products'] = products
        return context

    def form_valid(self, form):        
        org_pk = self.kwargs['pk']
        org = Org.objects.get(pk=org_pk)
        form.instance.org = org
        
        current_user = self.request.user
        # Redirect user if they don't have permission
        if(not current_user.has_perm('create_prod', org)):
            return HttpResponseRedirect('/home/')

        product = form.save(commit=False)
        

        product.save()
        
        product.admins.add(self.request.user)

        return super(ProductCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs.update({
            'request' : self.request
        })
        return kwargs

    def get_success_url(self):
        org = self.object.org
        prod = self.object
        groupName = org.title + str(org.pk)
        orgUserGroup = Group.objects.get(name=groupName)
        assign_perm('view_prod', orgUserGroup, prod)
        current_user = self.request.user
        print current_user
        print prod
        assign_perm('products.delete_product', current_user, prod)
        assign_perm('products.change_product', current_user, prod)
        #if(current_user.has_perm('products.delete_product', prod)):
        #    print "User has product delete perm"

        return reverse('feature_create_home', args=(self.object.org.id,self.object.id))

class ProductUpdateView(LoginRequiredMixin, UpdateView):
#class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):    
    """
    Form to update a product
    """
    success_url = None
    template_name = "products/product-update.html"
    form_class = ProductUpdateForm
    model = Product
    permission_required = 'products.change_product'
    

    def get_context_data(self, **kwargs):
        """Use this to add extra context (the user)."""
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        product_pk = self.kwargs['pk']
        product = Product.objects.get(pk=product_pk)
        context['product'] = product


        user = self.request.user
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)

        user_orgs = user.orgs.all()
        org_products = org.products.all()
        prod_features = product.features.all()
        context['user'] = user
        context['org'] = org
        
        context['user_orgs'] = user_orgs
        context['org_products'] = org_products
        context['prod_features'] = prod_features

        return context



    def get_object(self):
        product_pk = self.kwargs['pk']
        current_product = Product.objects.get(pk=product_pk)
        return current_product

    def form_valid(self, form, *args, **kwargs):
        updated_product = form.save()
        updated_product.save()

        # Determine next move 
        org_pk = self.kwargs['opk']
        prod_pk = self.kwargs['pk']
        success_url = self.get_success_url(org_pk, prod_pk)
        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)
    '''
    def get_form_kwargs(self):
        kwargs = super(ProductUpdateView, self).get_form_kwargs()
        
        # Pass org accounts to form for experts choice
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        org_accounts = org.accounts.all().only('first_name', 'last_name')
        
        kwargs.update({
            'request' : self.request,
            'org_accounts' : org_accounts
        })
        return kwargs
    '''

    def get_success_url(self, org_id, prod_id):
        return reverse('product_home',args=(org_id, prod_id,))


    def form_invalid(self, form):
        # tl;dr -- this method is implemented to work around Django
        # ticket #25548, which is present in the Django 1.9 release
        # (but not in Django 1.8 or 1.10).
        #
        # The longer explanation is that in Django 1.9,
        # FormMixin.form_invalid() does not pass the form instance to
        # get_context_data(). This causes get_context_data() to
        # construct a new form instance with the same data in order to
        # put it into the template context, and then any access to
        # that form's ``errors`` or ``cleaned_data`` runs that form
        # instance's validation. The end result is that validation
        # gets run twice on an invalid form submission, which is
        # undesirable for performance reasons.
        #
        # Manually implementing this method, and passing the form
        # instance to get_context_data(), solves this issue (which was
        # fixed in Django 1.9.1 and so is not present in Django
        # 1.10).
        return self.render_to_response(self.get_context_data(form=form))



class ProductView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    
    """
    model = Product
    template_name = "products/product-home.html"
    permission_required = 'products.view_prod'

    def get_context_data(self, **kwargs):
        """Use this to add extra context (the user)."""
        context = super(ProductView, self).get_context_data(**kwargs)
        user = self.request.user
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        product_pk = self.kwargs['pk']
        product = Product.objects.get(pk=product_pk)
        user_orgs = user.orgs.all()
        org_products = org.products.all()
        prod_features = product.features.all()
        context['user'] = user
        context['org'] = org
        context['product'] = product
        context['user_orgs'] = user_orgs
        context['prod_features'] = prod_features
        context['org_products'] = org_products

        if(user in product.admins.all()):
            context['editable'] = True
        else:
            context['editable'] = False


        return context

    def get_user(self, username):        
        #Given the verified username, look up and return the
        #corresponding user account if it exists, or ``None`` if it
        #doesn't.
        User = get_user_model()
        lookup_kwargs = {
            User.USERNAME_FIELD: username,
        }
        try:
            user = User.objects.get(**lookup_kwargs)
            return user
        except User.DoesNotExist:
            return None
class ProductCreateFirstView(ProductCreateView):
    template_name = 'products/product-create-first.html'

    def get_success_url(self):
        org = self.object.org
        prod = self.object
        groupName = org.title + str(org.pk)
        orgUserGroup = Group.objects.get(name=groupName)
        assign_perm('view_prod', orgUserGroup, prod)
        current_user = self.request.user
        assign_perm('products.delete_product', current_user, prod)
        #if(current_user.has_perm('products.delete_product', prod)):
        #    print "User has product delete perm"

        return reverse('feature_create_first', args=(self.object.org.id,self.object.id))

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model=Product
    template_name = 'products/product-delete-confirm.html'
    permission_required = 'products.delete_product'

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)

        product = self.get_object()
        org = product.org

        context['org'] = org
        context['product'] = product

        return context
    
    def get_object(self, queryset=None):

        """ Hook to ensure object is owned by request.user. """
        obj = super(ProductDeleteView, self).get_object()
        #success_url = self.get_success_url
        if not obj.admins.filter(pk=self.request.user.id).exists():
            raise Http404
        return obj

    def get_success_url(self):
        success_url = reverse('org_home', args=(self.object.org.id,))
        return success_url




class FeatureListView(TemplateView):
    """
    
    """
    template_name = "features/feature-list-home.html"

    def get_context_data(self, **kwargs):
        """Use this to add extra context (the user)."""
        context = super(FeatureListView, self).get_context_data(**kwargs)
        user = self.request.user
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        product_pk = self.kwargs['ppk']
        product = Product.objects.get(pk=product_pk)
        user_orgs = user.orgs.all()
        org_products = org.products.all()
        prod_features = product.features.all()
        context['user'] = user
        context['org'] = org
        context['product'] = product
        context['user_orgs'] = user_orgs
        context['prod_features'] = prod_features
        context['org_products'] = org_products
        #print context
        return context

    def get_user(self, username):        
        #Given the verified username, look up and return the
        #corresponding user account if it exists, or ``None`` if it
        #doesn't.
        User = get_user_model()
        lookup_kwargs = {
            User.USERNAME_FIELD: username,
        }
        try:
            user = User.objects.get(**lookup_kwargs)
            return user
        except User.DoesNotExist:
            return None



class FeatureCreateView(LoginRequiredMixin, CreateView):
    model = Feature
    form_class = FeatureScreenshotForm
    template_name = 'features/feature-create-home.html'
    
    # Check that user has permission to create features in this org
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        feature_create_perm = user.has_perm('orgs.create_feat', org)
        if(not feature_create_perm):
            return redirect('/home/')
        return super(FeatureCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """Use this to add extra context (the user)."""
        context = super(FeatureCreateView, self).get_context_data(**kwargs)
        user = self.request.user
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        feature_create_perm = user.has_perm('orgs.create_feat', org);

        user_orgs = user.orgs.all()
        org_products = org.products.all()
        product_pk = self.kwargs['ppk']
        product = Product.objects.get(pk=product_pk)
        prod_features = product.features.all()
        context['user'] = user
        context['org'] = org
        context['product'] = product
        context['user_orgs'] = user_orgs
        context['org_products'] = org_products
        context['prod_features'] = prod_features

        all_org_accounts = org.accounts.all()
        #print "all_org_accounts"
        #print all_org_accounts
        #form_class.fields["experts"].queryset = all_org_accounts
        
        return context

    def form_valid(self, form):        
        product_pk = self.kwargs['ppk']
        product = Product.objects.get(pk=product_pk)
        form.instance.product = product
        
        org = product.org
        current_user = self.request.user
        # Redirect user if they don't have permission
        if(not current_user.has_perm('create_feat', org)):
            return HttpResponseRedirect('/home/')

        feature = form.save(commit=False)
        feature.save()
        feature.admins.add(self.request.user)
        print self.request.FILES
        if "screenshot" in self.request.FILES:
            print "Creating Screenshot object"
            screenshot = Screenshot(image=self.request.FILES['screenshot'])
            screenshot.title = self.request.FILES['screenshot']
            screenshot.save()
            screenshot.admins.add(self.request.user)
            feature.screenshots.add(screenshot)
        else:
            print "No Screenshot present"

        # Allow users in org to respond to questions about feature
        groupName = org.title + str(org.pk)
        orgUserGroup = Group.objects.get(name=groupName)
        assign_perm('create_response', orgUserGroup, feature)

        return super(FeatureCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(FeatureCreateView, self).get_form_kwargs()
        
        # Pass org accounts to form for experts choice
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        org_accounts = org.accounts.all().only('first_name', 'last_name')
        
        kwargs.update({
            'request' : self.request,
            'org_accounts' : org_accounts
        })
        return kwargs

    def get_success_url(self):
        prod = self.object.product
        org = prod.org
        feat = self.object
        groupName = org.title + str(org.pk)
        orgUserGroup = Group.objects.get(name=groupName)
        assign_perm('view_feat', orgUserGroup, feat)
        current_user = self.request.user
        print current_user
        print feat
        assign_perm('products.delete_feature', current_user, feat)
        assign_perm('products.change_feature', current_user, feat)

        return reverse('feature_home', args=(self.object.product.org.id,self.object.product.id,self.object.id))

class FeatureCreateFirstView(FeatureCreateView):
    template_name = 'features/feature-create-first.html'


class FeatureView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    
    """
    model = Feature
    template_name = "features/feature-home.html"
    permission_required = 'products.view_feat'

    def get_context_data(self, **kwargs):
        """Use this to add extra context (the user)."""
        context = super(FeatureView, self).get_context_data(**kwargs)
        user = self.request.user
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        product_pk = self.kwargs['ppk']
        product = Product.objects.get(pk=product_pk)
        feature_pk = self.kwargs['pk']
        feature = Feature.objects.get(pk=feature_pk)
        user_orgs = user.orgs.all()
        org_products = org.products.all()
        product_features = product.features.all()

        feature_screenshots = feature.screenshots.all()
        feature_experts = feature.experts.all()

        questions = Question.objects.filter(features=feature)
        context['user'] = user
        context['org'] = org
        context['product'] = product
        context['feature'] = feature
        context['user_orgs'] = user_orgs
        context['org_products'] = org_products
        context['prod_features'] = product_features
        context['questions'] = questions
        context['screenshots'] = feature_screenshots
        
        context['experts'] = feature_experts

        
        if(user in feature.admins.all()):
            context['editable'] = True
        else:
            context['editable'] = False


        # Get annotations for the first screenshot
        # TODO: Enable multiple screenshots and pass all anotations
        if(len(feature_screenshots) > 0):
            screenshot = feature_screenshots[0]
            annotations = []
            expert_annotations = [];
            other_annotations = [];
            annotationsSet = Annotation.objects.filter(screenshot = screenshot)

            
            # Serialize each annotation
            for annotation in annotationsSet:

                annotationAdmin = annotation.admin
                
                adminProfilePic = annotationAdmin.filename
                profile_pic_url = "/media/profile_pics/" + adminProfilePic
                adminName = annotationAdmin.username
                adminRole = annotationAdmin.role

                annotation.profilePic = profile_pic_url
                annotation.name = adminName
                annotation.role = adminRole
                annotation.save()

                serializedAnno = serializers.serialize('json', [ annotation, ])

                print serializedAnno
                # Divide expert and other annotations before JSON
                if(annotation.admin in feature.experts.all()):
                    expert_annotations.append(serializedAnno)
                else:
                    other_annotations.append(serializedAnno)
            annotations.append(expert_annotations)
            annotations.append(other_annotations)
            print "annotations: "
            print annotations
            context['annotations'] = annotationsSet
            # Json encoding
            annotations_json = json.dumps(annotations, cls=DjangoJSONEncoder)
            context['annotations_json'] = annotations_json

        return context

    def get_user(self, username):        
        #Given the verified username, look up and return the
        #corresponding user account if it exists, or ``None`` if it
        #doesn't.
        User = get_user_model()
        lookup_kwargs = {
            User.USERNAME_FIELD: username,
        }
        try:
            user = User.objects.get(**lookup_kwargs)
            return user
        except User.DoesNotExist:
            return None

class FeatureUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Form to update a feature
    """
    success_url = None
    template_name = "features/feature-update.html"
    form_class = FeatureScreenshotUpdateForm
    model = Feature
    permission_required = 'products.change_feature'
    

    def get_context_data(self, **kwargs):
        """Use this to add extra context (the user)."""
        context = super(FeatureUpdateView, self).get_context_data(**kwargs)
        feature_pk = self.kwargs['pk']
        feature = Feature.objects.get(pk=feature_pk)
        context['feature'] = feature


        user = self.request.user
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)

        user_orgs = user.orgs.all()
        org_products = org.products.all()
        product_pk = self.kwargs['ppk']
        product = Product.objects.get(pk=product_pk)
        prod_features = product.features.all()
        context['user'] = user
        context['org'] = org
        context['product'] = product
        context['user_orgs'] = user_orgs
        context['org_products'] = org_products
        context['prod_features'] = prod_features

        if feature.screenshots.count() > 0:
            context['screenshot'] = feature.screenshots.all()[0].image

        return context



    def get_object(self):
        feature_pk = self.kwargs['pk']
        current_feature = Feature.objects.get(pk=feature_pk)
        return current_feature

    def form_valid(self, form, *args, **kwargs):
        updated_feature = form.save()
        updated_feature.save()

        print "UPDATED!!"
        print form
        for expert in updated_feature.experts.all():
            print expert


        print "checking files"
        print self.request.FILES
        if "screenshot" in self.request.FILES:
            # Check for current screenshot and remove
            print "current screenshot count: "
            print updated_feature.screenshots.count()
            if updated_feature.screenshots.count() > 0:
                current_screenshot = updated_feature.screenshots.all()[0]
                updated_feature.screenshots.remove(current_screenshot)
            print "Creating Screenshot object"
            screenshot = Screenshot(image=self.request.FILES['screenshot'])
            screenshot.title = self.request.FILES['screenshot']
            screenshot.save()
            screenshot.admins.add(self.request.user)

            updated_feature.screenshots.add(screenshot)
        else:
            print "No Screenshot present"

        # Determine next move 
        org_pk = self.kwargs['opk']
        prod_pk = self.kwargs['ppk']
        feat_pk = self.kwargs['pk']
        success_url = self.get_success_url(org_pk, prod_pk, feat_pk)
        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def get_form_kwargs(self):
        kwargs = super(FeatureUpdateView, self).get_form_kwargs()
        
        # Pass org accounts to form for experts choice
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        org_accounts = org.accounts.all().only('first_name', 'last_name')
        
        kwargs.update({
            'request' : self.request,
            'org_accounts' : org_accounts
        })
        return kwargs
        

    def get_success_url(self, org_id, prod_id, feat_id):
        return reverse('feature_home',args=(org_id, prod_id, feat_id,))


    def form_invalid(self, form):
        # tl;dr -- this method is implemented to work around Django
        # ticket #25548, which is present in the Django 1.9 release
        # (but not in Django 1.8 or 1.10).
        #
        # The longer explanation is that in Django 1.9,
        # FormMixin.form_invalid() does not pass the form instance to
        # get_context_data(). This causes get_context_data() to
        # construct a new form instance with the same data in order to
        # put it into the template context, and then any access to
        # that form's ``errors`` or ``cleaned_data`` runs that form
        # instance's validation. The end result is that validation
        # gets run twice on an invalid form submission, which is
        # undesirable for performance reasons.
        #
        # Manually implementing this method, and passing the form
        # instance to get_context_data(), solves this issue (which was
        # fixed in Django 1.9.1 and so is not present in Django
        # 1.10).
        return self.render_to_response(self.get_context_data(form=form))




class FeatureDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model=Feature
    template_name = 'features/feature-delete-confirm.html'
    permission_required = 'products.delete_feature'

    def get_context_data(self, **kwargs):
        context = super(FeatureDeleteView, self).get_context_data(**kwargs)
        
        feature = self.get_object()
        product = feature.product
        org = product.org
        
        context['org'] = org
        context['product'] = product
        context['feature'] = feature

        return context
    
    def get_object(self, queryset=None):

        """ Hook to ensure object is owned by request.user. """
        obj = super(FeatureDeleteView, self).get_object()
        #success_url = self.get_success_url
        if not obj.admins.filter(pk=self.request.user.id).exists():
            raise Http404
        return obj

    def get_success_url(self):
        print "GET SUCCESS URL"
        success_url = reverse('product_home', args=(self.object.product.org.id,self.object.product.id))
        return success_url






class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class FeatureList(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

class FeatureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class LinkList(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer