# Generated by Django 3.1.12 on 2021-06-23 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_collection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metahubmycollectionpage',
            name='theme_color',
            field=models.CharField(choices=[('magenta', 'Magenta pink'), ('strawberry', 'Strawberry red'), ('sapphire', 'Sapphire blue'), ('phlox', 'Phlox purple')], default='magenta', max_length=100),
        ),
    ]
