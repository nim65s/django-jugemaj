# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 22:50
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='nom')),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='titre')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ended', models.BooleanField(default=False, verbose_name='fini')),
                ('end', models.DateTimeField(verbose_name='fin')),
                ('hide', models.BooleanField(default=False, verbose_name='cacher les votes avant la fin')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elector_name', models.CharField(max_length=250, null=True, verbose_name='votre nom')),
                ('choice', models.IntegerField(choices=[(1, 'Super'), (2, 'Bien'), (3, 'OK'), (4, 'Passable'), (5, 'Insuffisant'), (6, 'Nul')], null=True, verbose_name='choix')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jugemaj.Candidate')),
                ('elector_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jugemaj.Election'),
        ),
    ]
