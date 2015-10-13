# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('netdev', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendlist',
            name='main_user',
            field=models.ForeignKey(related_name='main_user', to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 20, 20, 58, 10, 757000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 20, 20, 58, 10, 750000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 20, 20, 58, 10, 756000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 20, 20, 58, 10, 750000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=1, verbose_name=b'gender', choices=[(b'H', b'Homem'), (b'M', b'Mulher')]),
            preserve_default=True,
        ),
    ]
