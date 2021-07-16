# Generated by Django 3.1.12 on 2021-07-16 12:05

from django.db import migrations
import starling.mixins
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('menu', '0001_initial'),
        ('wagtailsearchpromotions', '0002_capitalizeverbose'),
        ('collection', '0007_metahubobjectpage_subtitle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metahubobjectseriespage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='metahubobjectseriespage',
            name='promo_image',
        ),
        migrations.RemoveField(
            model_name='metahubobjectseriespage',
            name='share_image',
        ),
        migrations.RemoveField(
            model_name='metahubobjectseriespage',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='basecollectionobject',
            name='series_page',
        ),
        migrations.AlterField(
            model_name='metahubobjectpage',
            name='content',
            field=wagtail.core.fields.StreamField([('single_richtext', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock())])), ('two_column_picture_richtext', wagtail.core.blocks.StructBlock([('figure', wagtail.core.blocks.StructBlock([('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())])), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('text', wagtail.core.blocks.RichTextBlock(required=True))])), ('richtext_with_link', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock(required=True)), ('link', starling.mixins.OptionalBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('href', wagtail.core.blocks.StructBlock([('source', wagtail.core.blocks.StreamBlock([('page', wagtail.core.blocks.PageChooserBlock()), ('external', wagtail.core.blocks.URLBlock()), ('mail', wagtail.core.blocks.EmailBlock()), ('phone', wagtail.core.blocks.CharBlock())], max_num=1, min_num=1))]))])))])), ('video', wagtail.core.blocks.StructBlock([('video', wagtail.core.blocks.StructBlock([('video', wagtail.core.blocks.StructBlock([('src', wagtail.core.blocks.StreamBlock([('youtube', wagtail.core.blocks.StructBlock([('src', wagtail.core.blocks.URLBlock(role='source')), ('title', wagtail.core.blocks.CharBlock(role='title'))])), ('vimeo', wagtail.core.blocks.StructBlock([('src', wagtail.core.blocks.URLBlock(role='source')), ('title', wagtail.core.blocks.CharBlock(role='title'))]))], max_num=1, min_num=1))])), ('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())]))], required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('highlight', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=200)), ('link', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('href', wagtail.core.blocks.StructBlock([('source', wagtail.core.blocks.StreamBlock([('page', wagtail.core.blocks.PageChooserBlock()), ('external', wagtail.core.blocks.URLBlock()), ('mail', wagtail.core.blocks.EmailBlock()), ('phone', wagtail.core.blocks.CharBlock())], max_num=1, min_num=1))]))])), ('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())]))])), ('image_mosaic', wagtail.core.blocks.StructBlock([('figures', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())])), ('caption', wagtail.core.blocks.CharBlock(required=False))])))])), ('cookie_settings', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('text', wagtail.core.blocks.TextBlock())]))], blank=True),
        ),
        migrations.AlterField(
            model_name='metahubobjectpage',
            name='related_items',
            field=wagtail.core.fields.StreamField([('related_curated', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100)), ('items', wagtail.core.blocks.StructBlock([('pages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(page_type=['collection.MetaHubObjectPage'], required=False)))]))])), ('related_automatic', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100))]))], blank=True),
        ),
        migrations.DeleteModel(
            name='CollectionObjectSeriesTag',
        ),
        migrations.DeleteModel(
            name='MetaHubObjectSeriesPage',
        ),
    ]
