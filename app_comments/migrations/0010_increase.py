# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 22:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_comments', '0009_comment_reddit_parent_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Increase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.IntegerField(null=True)),
                ('child_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_increases', to='app_comments.Comment')),
                ('parent_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_increases', to='app_comments.Comment')),
            ],
        ),
    ]
