# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-22 13:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0003_auto_20170720_0721'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='org',
            options={'ordering': ('title',), 'permissions': (('view_org', 'View org'), ('create_prod', 'Create org product'))},
        ),
    ]
