# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-01 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]