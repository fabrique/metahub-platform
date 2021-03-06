# Generated by Django 3.1.12 on 2021-08-06 09:18

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0009_metahubobjectpage_location_page'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('locations', '0002_auto_20210716_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='metahublocationpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='locations.LocationTag', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='LocationObjectRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('location', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_object_relationship', to='locations.metahublocationpage')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_location_relationship', to='collection.metahubobjectpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
