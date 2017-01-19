from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from core.models import TimeStampedModel

class Org(TimeStampedModel):
    title = models.CharField(max_length=50)
    admin = models.ForeignKey('accounts.Account', related_name="admin_org")

    def __str__(self):
        return "%s" % (self.title)
    
    class Meta:
        ordering = ('title',)


class Expert(TimeStampedModel):
    account = models.OneToOneField('accounts.Account', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.account

    class Meta:
        ordering = ('account',)

class Skill(TimeStampedModel):
    title = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    experts = models.ManyToManyField(Expert, related_name='skills')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)