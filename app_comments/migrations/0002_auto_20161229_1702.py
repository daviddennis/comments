# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.RemoveField(
            model_name='comment',
            name='children',
        ),
        migrations.AddField(
            model_name='comment',
            name='children',
            field=models.ManyToManyField(to='app_comments.Comment'),
        ),
    ]
