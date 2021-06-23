# Generated by Django 3.2 on 2021-06-22 13:16

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20210622_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metahubcontentpage',
            name='related_items',
            field=wagtail.core.fields.StreamField([('related_curated', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100)), ('items', wagtail.core.blocks.StructBlock([('pages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(required=False)))]))]))], blank=True),
        ),
    ]