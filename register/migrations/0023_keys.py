# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0022_auto_20170103_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='KEYS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=120, null=True)),
                ('value', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
    ]