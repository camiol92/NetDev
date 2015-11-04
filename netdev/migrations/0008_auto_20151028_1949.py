# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('netdev', '0007_auto_20151028_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='filecategory',
            name='owner',
            field=models.ForeignKey(related_name='owner', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 49, 0, 484000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 49, 0, 487000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 49, 0, 482000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 49, 0, 486000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 21, 49, 0, 481000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
