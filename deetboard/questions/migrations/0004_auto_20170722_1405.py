# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-22 14:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_question_screenshots'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('created',), 'permissions': (('view_quest', 'View question'),)},
        ),
    ]