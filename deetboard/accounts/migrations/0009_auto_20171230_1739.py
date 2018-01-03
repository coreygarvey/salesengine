# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-30 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20170715_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='tooltip',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.FileField(blank=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(default='', max_length=50),
        ),
    ]