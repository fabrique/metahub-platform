# Generated by Django 3.1.12 on 2021-06-28 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20210623_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metahubnewspage',
            name='theme_color',
            field=models.CharField(choices=[('theme--magenta', 'Magenta pink'), ('theme--pink', 'Strawberry red'), ('theme--blue', 'Sapphire blue'), ('theme--purple', 'Phlox purple')], default='theme--magenta', max_length=100),
        ),
    ]
