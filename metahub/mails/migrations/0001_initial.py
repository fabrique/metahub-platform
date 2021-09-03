# Generated by Django 3.1.3 on 2021-02-01 14:37

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, unique=True)),
                ('text', wagtail.core.fields.RichTextField()),
            ],
        ),
    ]
