# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-11 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('auth', '0008_alter_user_username_max_length'),
        ('accounts', '0001_initial'),
        ('orgs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='features_following',
            field=models.ManyToManyField(null=True, related_name='followers', to='products.Feature'),
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='account',
            name='orgs',
            field=models.ManyToManyField(null=True, related_name='accounts', to='orgs.Org'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
