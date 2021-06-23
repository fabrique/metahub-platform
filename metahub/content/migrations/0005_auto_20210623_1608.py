# Generated by Django 3.1.12 on 2021-06-23 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_alter_metahubcontentpage_related_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metahubcontentpage',
            name='related_items',
        ),
        migrations.AddField(
            model_name='metahubcontentpage',
            name='theme_color',
            field=models.CharField(choices=[('magenta', 'Magenta pink'), ('strawberry', 'Strawberry red'), ('sapphire', 'Sapphire blue'), ('phlox', 'Phlox purple')], default='magenta', max_length=100),
        ),
    ]
