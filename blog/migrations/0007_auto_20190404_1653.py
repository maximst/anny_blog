# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-04 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20190305_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramblog',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='instagramblog',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='instagramimage',
            name='image',
            field=models.ImageField(blank=True, max_length=1024, null=True, upload_to=b'images'),
        ),
        migrations.AlterUniqueTogether(
            name='instagramblog',
            unique_together=set([('inst_id', 'category'), ('slug', 'category')]),
        ),
        migrations.AlterUniqueTogether(
            name='instagramimage',
            unique_together=set([('inst_id', 'blog')]),
        ),
    ]
