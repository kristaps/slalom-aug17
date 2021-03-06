# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-19 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_auto_20170819_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='address',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='airport_transfer_time',
            field=models.PositiveIntegerField(default=10800),
        ),
        migrations.AddField(
            model_name='provider',
            name='nearest_airport',
            field=models.CharField(default='rix', max_length=20),
            preserve_default=False,
        ),
    ]
