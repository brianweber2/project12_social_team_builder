# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20170501_2031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='expertise',
            new_name='related_skill',
        ),
        migrations.AddField(
            model_name='position',
            name='description',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='position',
            name='name',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='project',
            name='time_estimate',
            field=models.TextField(default=b''),
        ),
    ]