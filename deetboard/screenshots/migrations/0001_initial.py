# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-11 15:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('file_path', models.FileField(upload_to=b'')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenshots_admin', to=settings.AUTH_USER_MODEL)),
                ('feature', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='products.Feature')),
                ('question', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='screenshots', to='questions.Question')),
            ],
            options={
                'ordering': ('title',),
            },
        ),
    ]
