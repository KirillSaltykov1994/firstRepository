# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-11 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forStudents', '0008_auto_20200910_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='score',
            field=models.IntegerField(default=1),
        ),
    ]
