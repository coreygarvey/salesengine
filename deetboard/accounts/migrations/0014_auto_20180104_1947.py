# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-04 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_account_cc_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
