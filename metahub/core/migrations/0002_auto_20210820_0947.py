# Generated by Django 3.1.12 on 2021-08-20 09:47

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsettings',
            name='footer_content_simple_en',
            field=wagtail.core.fields.StreamField([('footer', wagtail.core.blocks.StructBlock([('footer_links', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('href', wagtail.core.blocks.StructBlock([('source', wagtail.core.blocks.StreamBlock([('page', wagtail.core.blocks.PageChooserBlock()), ('external', wagtail.core.blocks.URLBlock()), ('mail', wagtail.core.blocks.EmailBlock()), ('phone', wagtail.core.blocks.CharBlock())], max_num=1, min_num=1))]))])))]))], default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='globalsettings',
            name='footer_content_simple',
            field=wagtail.core.fields.StreamField([('footer', wagtail.core.blocks.StructBlock([('footer_links', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('href', wagtail.core.blocks.StructBlock([('source', wagtail.core.blocks.StreamBlock([('page', wagtail.core.blocks.PageChooserBlock()), ('external', wagtail.core.blocks.URLBlock()), ('mail', wagtail.core.blocks.EmailBlock()), ('phone', wagtail.core.blocks.CharBlock())], max_num=1, min_num=1))]))])))]))]),
        ),
    ]
