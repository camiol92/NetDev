# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('netdev', '0009_auto_20151031_2328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repofile',
            name='allowed_users',
        ),
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 13, 33, 48, 635000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 13, 33, 48, 639000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 13, 33, 48, 633000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 13, 33, 48, 638000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 13, 33, 48, 632000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
