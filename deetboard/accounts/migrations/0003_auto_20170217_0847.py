# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-17 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170211_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='features_following',
            field=models.ManyToManyField(related_name='followers', to='products.Feature'),
        ),
        migrations.AlterField(
            model_name='account',
            name='orgs',
            field=models.ManyToManyField(related_name='accounts', to='orgs.Org'),
        ),
    ]
