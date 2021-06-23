# Generated by Django 3.2 on 2021-06-22 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('wagtailcore', '0059_apply_collection_ordering'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaHubOverviewPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('promo_title', models.CharField(blank=True, help_text='Optioneel, wordt getoond in plaats van titel als deze pagina op andere plekken gelinkt wordt', max_length=100, verbose_name='Promo titel')),
                ('promo_intro', models.TextField(blank=True, help_text='Korte tekst die wordt getoond als deze pagina op andere plekken gelinkt wordt', verbose_name='Promo intro')),
                ('promo_link', models.CharField(blank=True, help_text="Tekst van het 'lees meer' linkje als deze pagina op andere plekken gelinkt wordt", max_length=50, verbose_name='Lees meer label')),
                ('twitter_hashtags', models.CharField(blank=True, help_text='Commagescheiden lijst van termen die als hashtag worden toegevoegd wanneer gedeeld op twitter, zonder de #', max_length=100, verbose_name='Twitter hashtags')),
                ('promo_image', models.ForeignKey(blank=True, help_text='Optioneel, wordt getoond als deze pagina op andere plekken gelinkt wordt', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.metahubimage', verbose_name='Promo afbeelding')),
                ('share_image', models.ForeignKey(blank=True, help_text='Optioneel, anders wordt promo afbeelding gebruikt, anders de pagina visual en anders de standaard deel afbeelding', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.metahubimage', verbose_name='Share afbeelding')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]