# Generated by Django 5.0.7 on 2024-08-13 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_invoice_status_alter_invoice_invoice_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='offer',
            name='delivery_timeline',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]