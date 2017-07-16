# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-16 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_feature_screenshots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='screenshots',
            field=models.ManyToManyField(related_name='features', to='screenshots.Screenshot'),
        ),
    ]