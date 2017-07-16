# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-07-16 09:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('screenshots', '0004_auto_20170716_0828'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('src', models.CharField(max_length=150)),
                ('text', models.TextField()),
                ('context', models.CharField(max_length=150)),
                ('shapeType', models.CharField(max_length=50)),
                ('style', models.CharField(max_length=150)),
                ('x_val', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('y_val', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('width', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('screenshot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to='screenshots.Screenshot')),
            ],
            options={
                'ordering': ('screenshot',),
            },
        ),
    ]