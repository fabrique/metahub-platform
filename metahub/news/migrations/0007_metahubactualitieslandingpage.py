# Generated by Django 3.1.12 on 2021-06-28 16:24

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('news', '0006_auto_20210628_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaHubActualitiesLandingPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('promo_title', models.CharField(blank=True, help_text='Optioneel, wordt getoond in plaats van titel als deze pagina op andere plekken gelinkt wordt', max_length=100, verbose_name='Promo titel')),
                ('promo_intro', models.TextField(blank=True, help_text='Korte tekst die wordt getoond als deze pagina op andere plekken gelinkt wordt', verbose_name='Promo intro')),
                ('promo_link', models.CharField(blank=True, help_text="Tekst van het 'lees meer' linkje als deze pagina op andere plekken gelinkt wordt", max_length=50, verbose_name='Lees meer label')),
                ('twitter_hashtags', models.CharField(blank=True, help_text='Commagescheiden lijst van termen die als hashtag worden toegevoegd wanneer gedeeld op twitter, zonder de #', max_length=100, verbose_name='Twitter hashtags')),
                ('theme_color', models.CharField(choices=[('theme--magenta', 'Magenta pink'), ('theme--pink', 'Strawberry red'), ('theme--blue', 'Sapphire blue'), ('theme--purple', 'Phlox purple')], default='theme--magenta', max_length=100)),
                ('header', wagtail.core.fields.StreamField([('header', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=200)), ('featured_item', wagtail.core.blocks.PageChooserBlock())]))])),
                ('promo_image', models.ForeignKey(blank=True, help_text='Optioneel, wordt getoond als deze pagina op andere plekken gelinkt wordt', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.metahubimage', verbose_name='Promo afbeelding')),
                ('share_image', models.ForeignKey(blank=True, help_text='Optioneel, anders wordt promo afbeelding gebruikt, anders de pagina visual en anders de standaard deel afbeelding', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.metahubimage', verbose_name='Share afbeelding')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]
