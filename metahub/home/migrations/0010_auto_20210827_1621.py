# Generated by Django 3.1.12 on 2021-08-27 16:21

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20210816_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='metahubhomepage',
            name='places_map',
            field=wagtail.core.fields.StreamField([('places_map', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='Title')), ('link_borneplatz_href_block', wagtail.core.blocks.PageChooserBlock()), ('link_alter_href_block', wagtail.core.blocks.PageChooserBlock()), ('link_toraschrein_href_block', wagtail.core.blocks.PageChooserBlock())]))], blank=True),
        ),
        migrations.AlterField(
            model_name='metahubhomepage',
            name='object_highlights',
            field=wagtail.core.fields.StreamField([('object_highlights', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100)), ('items', wagtail.core.blocks.StructBlock([('pages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(required=False)))]))], defaults={'classes': 'relevant-objects--home'}, required=False))], blank=True),
        ),
        migrations.AlterField(
            model_name='metahubhomepage',
            name='theme_color',
            field=models.CharField(choices=[('theme--pink', 'Magenta pink'), ('theme--magenta', 'Strawberry red'), ('theme--blue', 'Sapphire blue'), ('theme--purple', 'Royal purple')], default='theme--pink', max_length=100),
        ),
        migrations.AlterField(
            model_name='metahubmuseumsubhomepage',
            name='theme_color',
            field=models.CharField(choices=[('theme--pink', 'Magenta pink'), ('theme--magenta', 'Strawberry red'), ('theme--blue', 'Sapphire blue'), ('theme--purple', 'Royal purple')], default='theme--pink', max_length=100),
        ),
    ]