# Generated by Django 3.1.3 on 2021-03-10 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0004_auto_20210310_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Internal title'),
        ),
    ]
