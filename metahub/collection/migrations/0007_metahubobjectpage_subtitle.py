# Generated by Django 3.1.12 on 2021-06-29 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0006_metahubobjectpage_related_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='metahubobjectpage',
            name='subtitle',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]