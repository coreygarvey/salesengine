# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-22 14:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20170722_1352'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feature',
            options={'ordering': ('title',), 'permissions': (('view_feat', 'View feature'),)},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('title',), 'permissions': (('view_prod', 'View product'),)},
        ),
    ]