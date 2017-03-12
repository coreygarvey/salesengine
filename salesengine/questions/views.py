from django.shortcuts import render
from models import Question, Response
from serializers import QuestionSerializer, ResponseSerializer
from rest_framework import generics
from django.views.generic import CreateView, TemplateView

from django.http import HttpResponse
from django.views import View
import services
from forms import QuestionForm
from braces.views import LoginRequiredMixin
from orgs.models import Org
from products.models import Product, Feature
from django.core.urlresolvers import reverse


class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = 'questions/question-create-home.html'
    
    def get_context_data(self, **kwargs):
        """Use this to add extra context (the user)."""
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        user = self.request.user
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        user_orgs = user.orgs.all()
        products = org.products.all()
        product_pk = self.kwargs['ppk']
        product = Product.objects.get(pk=product_pk)
        features = product.features.all()
        feature_pk = self.kwargs['fpk']
        feature = Feature.objects.get(pk=feature_pk)
        context['user'] = user
        context['org'] = org
        context['user_orgs'] = user_orgs
        context['org_products'] = products
        context['product'] = product
        context['prod_features'] = features
        context['feature'] = feature
        return context

    def form_valid(self, form):        
        prod_pk = self.kwargs['ppk']
        product = Product.objects.get(pk=prod_pk)
        form.instance.product = product
        form.instance.user_asking = self.request.user
        form.instance.admin = self.request.user

        question = form.save(commit=False)
        question.save()

        return super(QuestionCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(QuestionCreateView, self).get_form_kwargs()
        kwargs.update({
            'request' : self.request
        })
        return kwargs

    def get_success_url(self):
    	question_pk = self.object.id
        question = Question.objects.get(pk=question_pk)
        feature_pk = self.kwargs['fpk']
        feature = Feature.objects.get(pk=feature_pk)
        question.features.add(feature)
        return reverse('question_home', 
        			args=(
        				self.object.product.org.id,
        				self.object.product.id,
        				self.object.id
        				)
        			)

class QuestionView(TemplateView):
    """
    
    """
    template_name = "questions/question-home.html"

    def get_context_data(self, **kwargs):
        """Use this to add extra context (the user)."""
        context = super(QuestionView, self).get_context_data(**kwargs)
        user = self.request.user
        org_pk = self.kwargs['opk']
        org = Org.objects.get(pk=org_pk)
        product_pk = self.kwargs['ppk']
        product = Product.objects.get(pk=product_pk)
        user_orgs = user.orgs.all()
        org_products = org.products.all()
        prod_features = product.features.all()
        question_pk = self.kwargs['qpk']
        question = Question.objects.get(pk=question_pk)
        question_features = question.features.all()
        context['user'] = user
        context['org'] = org
        context['product'] = product
        context['user_orgs'] = user_orgs
        context['prod_features'] = prod_features
        context['org_products'] = org_products
        context['question'] = question
        context['question_features'] = question_features
        print context
        return context

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ResponseList(generics.ListCreateAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class ResponseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer