# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-15 04:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='scheduled_post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_text', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('message_type', models.CharField(max_length=20)),
                ('json_extra', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='scheduled_post_report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_sended', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=20)),
                ('scheduled_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.scheduled_post')),
            ],
        ),
        migrations.CreateModel(
            name='survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_name', models.CharField(max_length=250)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('for_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='survey_submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.survey')),
            ],
        ),
        migrations.CreateModel(
            name='survey_submission_value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('survey_submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.survey_submission')),
            ],
        ),
        migrations.CreateModel(
            name='survey_value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('type', models.CharField(max_length=20)),
                ('options', models.TextField()),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.survey')),
            ],
        ),
        migrations.CreateModel(
            name='user_account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=20)),
                ('short_memory', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='survey_submission_value',
            name='survey_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.survey_value'),
        ),
        migrations.AddField(
            model_name='survey_submission',
            name='user_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.user_account'),
        ),
    ]
