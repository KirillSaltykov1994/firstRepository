# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-09 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forStudents', '0002_question_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='right',
            field=models.BooleanField(default=False),
        ),
    ]
