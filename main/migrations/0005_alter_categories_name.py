# Generated by Django 5.0.7 on 2024-08-05 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_categories_product_vote_ratio_product_vote_total_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]