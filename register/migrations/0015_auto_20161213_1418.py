# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-13 14:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0014_auto_20161213_1409'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam_center_data',
            old_name='exam_center',
            new_name='exam_centre',
        ),
    ]
