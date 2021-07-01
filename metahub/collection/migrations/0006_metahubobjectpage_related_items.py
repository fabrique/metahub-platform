# Generated by Django 3.1.12 on 2021-06-29 15:47

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_auto_20210629_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='metahubobjectpage',
            name='related_items',
            field=wagtail.core.fields.StreamField([('related_curated', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100)), ('items', wagtail.core.blocks.StructBlock([('pages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(required=False)))]))])), ('related_automatic', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100))]))], blank=True),
        ),
    ]