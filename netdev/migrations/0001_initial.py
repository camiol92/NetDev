# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import netdev.models
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
            name='FileCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of the category. 100 chars maximum.', max_length=100, verbose_name='Nome do Diretorio')),
                ('description', models.TextField(verbose_name='Descricao do arquivo')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_mod', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(related_name='owner', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'FileCategory',
                'verbose_name_plural': 'FileCategories',
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
                ('date', models.DateTimeField(default=netdev.models.get_inf_time)),
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
                ('creation_date', models.DateTimeField(default=netdev.models.get_inf_time)),
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
            name='RepoFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Esse vai ser o nome visivel do arquivo.', max_length=250, verbose_name='Nome', error_messages={b'required': b'necessario'})),
                ('description', models.TextField(verbose_name='Descricao do arquivo')),
                ('front', models.ImageField(default=b'images/file_icon.png', upload_to=b'images/', null=True, verbose_name='Imagem para o arquivo', blank=True)),
                ('stored_file', models.FileField(help_text='Tamanho maximo 104Mb', upload_to=b'files/', verbose_name='Arquivo', error_messages={b'erro': b'Adicione um Arquivo'})),
                ('public', models.BooleanField(default=False, help_text='Selecione para tornar o arquivo publico.', verbose_name='Tornar Publico')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('last_mod', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(related_name='author', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('category', models.ForeignKey(related_name='files', verbose_name='Selecione o Diretorio', to='netdev.FileCategory')),
            ],
            options={
                'ordering': ['name'],
                'get_latest_by': 'pubdate',
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatusUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=netdev.models.get_inf_time)),
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
                ('creation_date', models.DateTimeField(default=netdev.models.get_inf_time)),
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
                ('display_name', models.CharField(max_length=100, verbose_name='Nome do Exibicao')),
                ('picture', models.ImageField(default=b'profile_images/default_avatar.png', upload_to=b'profile_images', verbose_name='Foto de Perfil')),
                ('gender', models.CharField(max_length=1, verbose_name='Genero', choices=[(b'H', b'Homem'), (b'M', b'Mulher')])),
                ('creation_date', models.DateTimeField(default=netdev.models.get_inf_time)),
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
            model_name='category',
            name='subforum',
            field=models.ForeignKey(related_name='categorys', to='netdev.SubForum'),
            preserve_default=True,
        ),
    ]
