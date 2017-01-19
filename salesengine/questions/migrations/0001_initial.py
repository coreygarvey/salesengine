# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 23:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orgs', '0002_auto_20161220_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_admin', to=settings.AUTH_USER_MODEL)),
                ('features', models.ManyToManyField(related_name='questions', to='products.Feature')),
                ('skills', models.ManyToManyField(related_name='questions', to='orgs.Skill')),
                ('user_asking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions_asked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('test', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses_admin', to=settings.AUTH_USER_MODEL)),
                ('question', models.ManyToManyField(related_name='responses', to='questions.Question')),
                ('user_responder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('accepted', 'created'),
            },
        ),
    ]
