# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('netdev', '0006_auto_20151028_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 33, 2, 520000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 33, 2, 523000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='front',
            field=models.ImageField(default=b'images/file_icon.png', upload_to=b'images/', null=True, verbose_name='Imagem para o arquivo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 33, 2, 518000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 33, 2, 522000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 33, 2, 517000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
