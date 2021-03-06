# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-26 20:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kredit', '0004_kredit_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='KreditRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(default='black', max_length=16, verbose_name='Color')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('stage', models.IntegerField(default=0, verbose_name='Stage')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('blinded_comment', models.TextField(blank=True, null=True, verbose_name='Blinded comment')),
                ('hide_comment', models.BooleanField(default=False, verbose_name='Hide comment')),
                ('session', models.CharField(blank=True, max_length=64, null=True)),
                ('cur_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kreditroute_curgroup', to='auth.Group', verbose_name='Current group')),
                ('cur_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kreditroute_curuser', to=settings.AUTH_USER_MODEL, verbose_name='Current user')),
                ('kredit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kredit.Kredit')),
                ('next_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kreditroute_nextgroup', to='auth.Group', verbose_name='Next group')),
                ('prev_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kreditroute_prevgroup', to='auth.Group', verbose_name='Previous group')),
            ],
            options={
                'verbose_name': 'Kredit route',
                'verbose_name_plural': 'Kredit routes',
            },
        ),
    ]
