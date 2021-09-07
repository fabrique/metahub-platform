# Generated by Django 3.1.12 on 2021-09-07 19:01

from django.db import migrations, models
import django.db.models.deletion
import starling.mixins
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210820_0947'),
        ('collection', '0010_remove_metahubobjectpage_location_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basecollectionartist',
            name='bc_change_date',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='basecollectionartist',
            name='bc_change_user',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='basecollectionartist',
            name='bc_date_acquired',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='metahubobjectpage',
            name='content',
            field=wagtail.core.fields.StreamField([('single_richtext', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(help_text='Optional, to use as an anchor in the page', max_length=100, required=False)), ('text', wagtail.core.blocks.RichTextBlock())])), ('two_column_picture_richtext', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(help_text='Optional, to use as an anchor in the page', max_length=100, required=False)), ('figure', wagtail.core.blocks.StructBlock([('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())], crop=False, resolution=('4096', '', '', '', '', '', True, True, False))), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('text', wagtail.core.blocks.RichTextBlock(required=True))])), ('richtext_with_link', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(help_text='Optional, to use as an anchor in the page', max_length=100, required=False)), ('text', wagtail.core.blocks.RichTextBlock(required=True)), ('link', starling.mixins.OptionalBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('href', wagtail.core.blocks.StructBlock([('source', wagtail.core.blocks.StreamBlock([('page', wagtail.core.blocks.PageChooserBlock()), ('external', wagtail.core.blocks.URLBlock()), ('mail', wagtail.core.blocks.EmailBlock()), ('phone', wagtail.core.blocks.CharBlock())], max_num=1, min_num=1))]))])))])), ('video', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(help_text='Optional, to use as an anchor in the page', max_length=100, required=False)), ('video', wagtail.core.blocks.StructBlock([('video', wagtail.core.blocks.StructBlock([('src', wagtail.core.blocks.StreamBlock([('youtube', wagtail.core.blocks.StructBlock([('src', wagtail.core.blocks.URLBlock(role='source')), ('title', wagtail.core.blocks.CharBlock(role='title'))])), ('vimeo', wagtail.core.blocks.StructBlock([('src', wagtail.core.blocks.URLBlock(role='source')), ('title', wagtail.core.blocks.CharBlock(role='title'))]))], max_num=1, min_num=1))])), ('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())], resolution=('1080x1050', '', '', '', '', '', True, True, False)))], required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('highlight', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(help_text='Optional, to use as an anchor in the page', max_length=100, required=False)), ('title', wagtail.core.blocks.CharBlock(max_length=200)), ('link', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('href', wagtail.core.blocks.StructBlock([('source', wagtail.core.blocks.StreamBlock([('page', wagtail.core.blocks.PageChooserBlock()), ('external', wagtail.core.blocks.URLBlock()), ('mail', wagtail.core.blocks.EmailBlock()), ('phone', wagtail.core.blocks.CharBlock())], max_num=1, min_num=1))]))])), ('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())], resolution=('4096', '', '', '', '', '', False, True, False)))])), ('image_mosaic', wagtail.core.blocks.StructBlock([('id', wagtail.core.blocks.CharBlock(help_text='Optional, to use as an anchor in the page', max_length=100, required=False)), ('figures', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())], crop=False, resolution=('4096', '', '', '', '', '', True, True, False))), ('caption', wagtail.core.blocks.CharBlock(required=False))])))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='metahubobjectpage',
            name='related_items',
            field=wagtail.core.fields.StreamField([('related_curated', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100)), ('items', wagtail.core.blocks.StructBlock([('pages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(required=False)))]))])), ('related_automatic', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='metahubobjectpage',
            name='theme_color',
            field=models.CharField(choices=[('theme--pink', 'Magenta pink'), ('theme--magenta', 'Strawberry red'), ('theme--blue', 'Sapphire blue'), ('theme--purple', 'Royal purple')], default='theme--pink', max_length=100),
        ),
        migrations.AlterField(
            model_name='objectimagelink',
            name='collection_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_img_link', to='collection.basecollectionobject'),
        ),
        migrations.AlterField(
            model_name='objectimagelink',
            name='object_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_img_link', to='core.metahubimage'),
        ),
    ]
