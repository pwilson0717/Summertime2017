# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-02 17:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pokee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gotPoked', to='login.User')),
                ('poker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poked', to='login.User')),
            ],
        ),
    ]
