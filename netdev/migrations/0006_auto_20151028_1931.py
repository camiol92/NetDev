# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import netdev.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('netdev', '0005_auto_20151028_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 31, 4, 635000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 31, 4, 638000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='allowed_users',
            field=models.ManyToManyField(related_name='allowed_users', to=settings.AUTH_USER_MODEL, blank=True, help_text='Selecione os usuarios que podem ver esse arquivo.', null=True, verbose_name='Usuarios Permitidos'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='front',
            field=netdev.fields.StdImageField(default=b'images/file_icon.png', upload_to=b'images/', null=True, verbose_name='Imagem para o arquivo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='public',
            field=models.BooleanField(default=False, help_text='Selecione para tornar o arquivo publico.', verbose_name='Tornar Publico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='stored_file',
            field=models.FileField(help_text='Tamanho maximo 104Mb', upload_to=b'files/', null=True, verbose_name='Arquivo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 31, 4, 634000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 31, 4, 638000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 31, 4, 632000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
