# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-08 09:52
from __future__ import unicode_literals

import blog.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190109_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='views_count',
            field=models.PositiveIntegerField(default=blog.utils.get_default_views_count),
        ),
    ]