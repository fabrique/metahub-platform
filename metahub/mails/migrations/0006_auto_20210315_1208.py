# Generated by Django 3.1.3 on 2021-03-15 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0005_mail_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='text',
            field=models.TextField(help_text='Add variables with double accolades, like Hello, {{ first_name }}! Available variables depend on the form being sent.'),
        ),
    ]
