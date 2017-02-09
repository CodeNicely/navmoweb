# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-13 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='admit_card_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refrence_id', models.CharField(blank=True, max_length=10, null=True)),
                ('date', models.CharField(blank=True, max_length=120, null=True)),
                ('time', models.CharField(blank=True, max_length=120, null=True)),
                ('center', models.CharField(blank=True, max_length=120, null=True)),
                ('city', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='second_round_admit_card_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refrence_id', models.CharField(blank=True, max_length=10, null=True)),
                ('current_round', models.CharField(blank=True, choices=[('First', 'First Round'), ('Semi-Finals', 'Semi Finals'), ('Finals', 'Finals')], max_length=120, null=True)),
                ('gamma_group_one', models.BooleanField(default=False)),
                ('alpha_beta_theta_group_two', models.BooleanField(default=False)),
                ('exam_center', models.CharField(blank=True, default=None, max_length=120, null=True)),
            ],
        ),
    ]