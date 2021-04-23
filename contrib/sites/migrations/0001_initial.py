# -*- coding: utf-8 -*-
from django.db import models, migrations
import django.contrib.sites.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('domain', models.CharField(max_length=100, unique=True, validators=[django.contrib.sites.models._simple_domain_name_validator], verbose_name='domain name')),
                ('name', models.CharField(verbose_name='display name', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'sites',
                'verbose_name': 'site',
                'db_table': 'django_site',
                'ordering': ('domain',),
            },
            managers=[
                ('objects', django.contrib.sites.models.SiteManager()),
            ],
        ),
    ]
