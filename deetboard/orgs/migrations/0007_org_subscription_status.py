# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-02 22:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0006_auto_20180102_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='subscription_status',
            field=models.CharField(default='Active', max_length=30),
            preserve_default=False,
        ),
    ]
