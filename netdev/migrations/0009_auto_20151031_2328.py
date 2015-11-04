# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('netdev', '0008_auto_20151028_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filecategory',
            name='description',
            field=models.TextField(verbose_name='Descricao do arquivo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='filecategory',
            name='name',
            field=models.CharField(help_text='Name of the category. 100 chars maximum.', max_length=100, verbose_name='Nome do Diretorio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 1, 28, 35, 238000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 1, 28, 35, 241000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 1, 28, 35, 236000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 1, 28, 35, 240000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 1, 28, 35, 234000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
