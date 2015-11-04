# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import netdev.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('netdev', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of the category. 100 chars maximum.', max_length=100, verbose_name='FileCategory name')),
                ('description', models.TextField(verbose_name='Description')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_mod', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'FileCategory',
                'verbose_name_plural': 'FileCategories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepoFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='This will be the visible name of the file.', max_length=250, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description of the file')),
                ('front', netdev.fields.StdImageField(null=True, upload_to=b'images/', blank=True)),
                ('stored_file', models.FileField(help_text='No maximum file size.', upload_to=b'files/', null=True, verbose_name='File to upload', blank=True)),
                ('public', models.BooleanField(default=False, help_text='Selecting this will make the file available to public.', verbose_name='Make public')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_mod', models.DateTimeField(auto_now_add=True)),
                ('allowed_users', models.ManyToManyField(related_name='allowed_users', to=settings.AUTH_USER_MODEL, blank=True, help_text='Select the users that can see this file.', null=True, verbose_name='Allowed users')),
                ('author', models.ForeignKey(related_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('category', models.ForeignKey(verbose_name='Select the category', to='netdev.FileCategory')),
            ],
            options={
                'ordering': ['name'],
                'get_latest_by': 'pubdate',
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 17, 38, 17, 87000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 17, 38, 17, 90000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 17, 38, 17, 85000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 17, 38, 17, 90000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 17, 38, 17, 84000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
