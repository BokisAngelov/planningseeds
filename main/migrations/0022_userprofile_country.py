# Generated by Django 5.1.1 on 2024-10-22 18:35

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_categories_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]
