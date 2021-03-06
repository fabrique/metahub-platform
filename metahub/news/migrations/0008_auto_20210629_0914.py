# Generated by Django 3.1.12 on 2021-06-29 09:14

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_metahubactualitieslandingpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metahubactualitieslandingpage',
            name='header',
            field=wagtail.core.fields.StreamField([('header', wagtail.core.blocks.StructBlock([('featured_item', wagtail.core.blocks.StructBlock([('page', wagtail.core.blocks.PageChooserBlock(required=False))])), ('excerpt', wagtail.core.blocks.TextBlock()), ('link_label', wagtail.core.blocks.CharBlock(default='Read more'))]))]),
        ),
    ]
