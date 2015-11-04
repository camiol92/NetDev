# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('position', models.IntegerField(default=0, verbose_name='Position')),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('position', models.IntegerField(default=0, verbose_name='Position')),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Friendlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friends', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('main_user', models.ForeignKey(related_name='main_user', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('text', models.TextField()),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 10, 24, 14, 59, 26, 144000, tzinfo=utc))),
                ('is_trash', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(verbose_name='Body')),
                ('views', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2015, 10, 24, 14, 59, 26, 152000, tzinfo=utc))),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'ordering': ['created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job', models.CharField(max_length=100, blank=True)),
                ('location', models.CharField(max_length=100, blank=True)),
                ('experience', models.TextField(blank=True)),
                ('academics', models.TextField(blank=True)),
                ('tags', models.TextField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatusUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 10, 24, 14, 59, 26, 139000, tzinfo=utc))),
                ('text', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubForum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('position', models.IntegerField(default=0, verbose_name='Position')),
                ('forum', models.ForeignKey(related_name='subforuns', to='netdev.Forum')),
            ],
            options={
                'ordering': ['position'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Name')),
                ('text', models.TextField()),
                ('views', models.IntegerField(default=0)),
                ('replies', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2015, 10, 24, 14, 59, 26, 151000, tzinfo=utc))),
                ('is_closed', models.BooleanField(default=False, verbose_name='Is closed')),
                ('category', models.ForeignKey(related_name='topics', to='netdev.Category')),
                ('last_post', models.ForeignKey(related_name='forum_last_post', verbose_name='Last post', blank=True, to='netdev.Post', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-last_post__created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=100)),
                ('picture', models.ImageField(default=b'profile_images/default_avatar.png', upload_to=b'profile_images')),
                ('gender', models.CharField(max_length=1, verbose_name=b'gender', choices=[(b'H', b'Homem'), (b'M', b'Mulher')])),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2015, 10, 24, 14, 59, 26, 138000, tzinfo=utc))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(related_name='posts', to='netdev.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(related_name='forum_posts', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='netdev.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='subforum',
            field=models.ForeignKey(related_name='categorys', to='netdev.SubForum'),
            preserve_default=True,
        ),
    ]
