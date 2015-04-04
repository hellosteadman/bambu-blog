# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers
import bambu_attachments.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ('name',),
                'db_table': 'blog_category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('slug', models.SlugField(max_length=100)),
                ('date', models.DateTimeField(db_index=True)),
                ('published', models.BooleanField(default=True)),
                ('broadcast', models.BooleanField(default=False, editable=False)),
                ('body', models.TextField()),
                ('excerpt', models.TextField(null=True, editable=False, blank=True)),
                ('css', models.TextField(null=True, blank=True)),
                ('author', models.ForeignKey(related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(related_name='posts', to='bambu_blog.Category', blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-date',),
                'db_table': 'blog_post',
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='PostUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(max_length=255, upload_to=bambu_attachments.helpers.upload_attachment_file)),
                ('url', models.CharField(max_length=255, db_index=True)),
                ('size', models.PositiveIntegerField(editable=False)),
                ('mimetype', models.CharField(max_length=50, editable=False, db_index=True)),
            ],
            options={
                'db_table': 'blog_post_upload',
            },
        ),
    ]
