# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-09 11:21
from __future__ import unicode_literals

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0010_auto_20180414_2058'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
                ('body', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(max_length=128, unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('edit_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(max_length=128, unique=True)),
                ('deleted', models.BooleanField(default=False)),
                ('front_page', models.BooleanField(default=True)),
                ('on_top', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('edit_time', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('image_rows', models.PositiveIntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10')], default=1, max_length=2)),
                ('video', models.URLField(blank=True, default=b'')),
                ('poll', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='poll.Poll')),
            ],
            options={
                'abstract': False,
                'base_manager_name': '_plain_manager',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('_plain_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=b'', max_length=128)),
                ('image', models.ImageField(max_length=1024, upload_to=b'images')),
                ('front_page', models.BooleanField(default=True)),
                ('order', models.IntegerField(blank=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (64, 64), (65, 65), (66, 66), (67, 67), (68, 68), (69, 69), (70, 70), (71, 71), (72, 72), (73, 73), (74, 74), (75, 75), (76, 76), (77, 77), (78, 78), (79, 79), (80, 80), (81, 81), (82, 82), (83, 83), (84, 84), (85, 85), (86, 86), (87, 87), (88, 88), (89, 89), (90, 90), (91, 91), (92, 92), (93, 93), (94, 94), (95, 95), (96, 96), (97, 97), (98, 98), (99, 99)], default=0)),
                ('ext_url', models.URLField(blank=True, max_length=2048, null=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='BlogTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('preview', models.TextField(blank=True, default=b'')),
                ('body', models.TextField(default=b'')),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='blog.Blog')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'blog_blog_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default=b'', max_length=64)),
                ('body', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('edit_time', models.DateTimeField(auto_now=True)),
                ('ip', models.GenericIPAddressField(default=b'127.0.0.1')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='filer.File')),
            ],
            bases=('filer.file',),
        ),
    ]
