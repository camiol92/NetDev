# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('netdev', '0004_auto_20151028_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 15, 6, 106000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 15, 6, 110000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='category',
            field=models.ForeignKey(verbose_name='Selecione o Diretorio', to='netdev.FileCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='description',
            field=models.TextField(verbose_name='Descricao do arquivo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='name',
            field=models.CharField(help_text='Esse vai ser o nome visivel do arquivo.', max_length=250, verbose_name='Nome'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='public',
            field=models.BooleanField(default=False, help_text='Selecione para tornar o arquivo publico.', verbose_name='Make public'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='repofile',
            name='stored_file',
            field=models.FileField(help_text='No maximum file size.', upload_to=b'files/', null=True, verbose_name='Arquivo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statusupdate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 15, 6, 104000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='topic',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 15, 6, 109000, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 28, 19, 15, 6, 101000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
