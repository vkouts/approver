# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-20 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kredit', '0002_auto_20160218_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sess', models.CharField(blank=True, max_length=64, null=True)),
                ('path_to', models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d/')),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
