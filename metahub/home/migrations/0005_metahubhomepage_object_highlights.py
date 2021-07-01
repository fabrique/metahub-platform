# Generated by Django 3.1.12 on 2021-07-01 14:50

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_metahubhomepage_home_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='metahubhomepage',
            name='object_highlights',
            field=wagtail.core.fields.StreamField([('object_highlights', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100))]))], default=''),
            preserve_default=False,
        ),
    ]