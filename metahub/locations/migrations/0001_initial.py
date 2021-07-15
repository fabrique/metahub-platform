# Generated by Django 3.1.12 on 2021-07-15 16:09

from django.db import migrations, models
import django.db.models.deletion
import starling.mixins
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailmodelchooser.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('wagtailcore', '0059_apply_collection_ordering'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaHubLocationPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('promo_title', models.CharField(blank=True, help_text='Optioneel, wordt getoond in plaats van titel als deze pagina op andere plekken gelinkt wordt', max_length=100, verbose_name='Promo titel')),
                ('promo_intro', models.TextField(blank=True, help_text='Korte tekst die wordt getoond als deze pagina op andere plekken gelinkt wordt', verbose_name='Promo intro')),
                ('promo_link', models.CharField(blank=True, help_text="Tekst van het 'lees meer' linkje als deze pagina op andere plekken gelinkt wordt", max_length=50, verbose_name='Lees meer label')),
                ('twitter_hashtags', models.CharField(blank=True, help_text='Commagescheiden lijst van termen die als hashtag worden toegevoegd wanneer gedeeld op twitter, zonder de #', max_length=100, verbose_name='Twitter hashtags')),
                ('theme_color', models.CharField(choices=[('theme--magenta', 'Magenta pink'), ('theme--pink', 'Strawberry red'), ('theme--blue', 'Sapphire blue'), ('theme--purple', 'Phlox purple')], default='theme--magenta', max_length=100)),
                ('authors', wagtail.core.fields.StreamField([('author', wagtailmodelchooser.blocks.ModelChooserBlock(target_model='authors.author'))], blank=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200)),
                ('longitude', models.CharField(blank=True, max_length=200)),
                ('hero_header', wagtail.core.fields.StreamField([('header_image', wagtail.core.blocks.StructBlock([('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())], resolution=('1920x1080', '', '', '', '', '', True, True, False)))]))])),
                ('text_header', wagtail.core.fields.StreamField([('header_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=200)), ('text', wagtail.core.blocks.TextBlock(max_length=2000))]))])),
                ('content', wagtail.core.fields.StreamField([('single_richtext', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock())])), ('two_column_picture_richtext', wagtail.core.blocks.StructBlock([('figure', wagtail.core.blocks.StructBlock([('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())])), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('text', wagtail.core.blocks.RichTextBlock(required=True))])), ('richtext_with_link', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.RichTextBlock(required=True)), ('link', starling.mixins.OptionalBlock(wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('href', wagtail.core.blocks.StructBlock([('source', wagtail.core.blocks.StreamBlock([('page', wagtail.core.blocks.PageChooserBlock()), ('external', wagtail.core.blocks.URLBlock()), ('mail', wagtail.core.blocks.EmailBlock()), ('phone', wagtail.core.blocks.CharBlock())], max_num=1, min_num=1))]))])))])), ('video', wagtail.core.blocks.StructBlock([('video', wagtail.core.blocks.StructBlock([('video', wagtail.core.blocks.StructBlock([('src', wagtail.core.blocks.StreamBlock([('youtube', wagtail.core.blocks.StructBlock([('src', wagtail.core.blocks.URLBlock(role='source')), ('title', wagtail.core.blocks.CharBlock(role='title'))])), ('vimeo', wagtail.core.blocks.StructBlock([('src', wagtail.core.blocks.URLBlock(role='source')), ('title', wagtail.core.blocks.CharBlock(role='title'))]))], max_num=1, min_num=1))])), ('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())]))], required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False))])), ('highlight', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=200)), ('link', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('href', wagtail.core.blocks.StructBlock([('source', wagtail.core.blocks.StreamBlock([('page', wagtail.core.blocks.PageChooserBlock()), ('external', wagtail.core.blocks.URLBlock()), ('mail', wagtail.core.blocks.EmailBlock()), ('phone', wagtail.core.blocks.CharBlock())], max_num=1, min_num=1))]))])), ('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())]))])), ('image_mosaic', wagtail.core.blocks.StructBlock([('figures', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('picture', wagtail.core.blocks.StructBlock([('source', wagtail.images.blocks.ImageChooserBlock())])), ('caption', wagtail.core.blocks.CharBlock(required=False))])))]))], blank=True)),
                ('related_items', wagtail.core.fields.StreamField([('related_curated', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100)), ('items', wagtail.core.blocks.StructBlock([('pages', wagtail.core.blocks.ListBlock(wagtail.core.blocks.PageChooserBlock(page_type=['stories.MetaHubStoryPage'], required=False)))]))])), ('related_automatic', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=100))]))], blank=True)),
                ('promo_image', models.ForeignKey(blank=True, help_text='Optioneel, wordt getoond als deze pagina op andere plekken gelinkt wordt', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.metahubimage', verbose_name='Promo afbeelding')),
                ('share_image', models.ForeignKey(blank=True, help_text='Optioneel, anders wordt promo afbeelding gebruikt, anders de pagina visual en anders de standaard deel afbeelding', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.metahubimage', verbose_name='Share afbeelding')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]