# Generated by Django 5.0.7 on 2024-08-09 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_invoice_options_alter_offer_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('Sent', 'Sent'), ('Accepted', 'Accepted')], default='Sent', max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_file',
            field=models.FileField(upload_to='docs/'),
        ),
    ]
