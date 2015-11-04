# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('netdev', '0012_auto_20151101_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 16, 4, 26, 998000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 16, 4, 27, 1000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='category',
            field=models.ForeignKey(related_name='files', verbose_name='Selecione o Diretorio', to='netdev.FileCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 16, 4, 26, 996000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 16, 4, 27, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 16, 4, 26, 995000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
