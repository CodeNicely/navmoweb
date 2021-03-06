# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-15 16:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0020_auto_20161214_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='topper_data',
            name='center',
            field=models.CharField(blank=True, choices=[('NH Goel', 'NH Goel'), ('ICIS', 'ICIS'), ('MPE Raipur', 'MPE Raipur')], default='NH Goel', max_length=120),
        ),
        migrations.AddField(
            model_name='topper_data',
            name='current_round',
            field=models.CharField(blank=True, choices=[('Semi-Finals', 'Semi-Finals'), ('Finals', 'Finals')], max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='topper_data',
            name='medal',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='topper_data',
            name='rank',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='topper_data',
            name='group',
            field=models.CharField(blank=True, choices=[('alpha', 'alpha'), ('beta', 'beta'), ('thetha', 'thetha'), ('gamma', 'gamma')], max_length=120),
        ),
    ]
