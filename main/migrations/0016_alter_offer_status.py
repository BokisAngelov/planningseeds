# Generated by Django 5.0.7 on 2024-08-08 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('In-progress', 'In-progress'), ('Accepted', 'Accepted'), ('Declined', 'Declined')], default='In-progress', max_length=20),
        ),
    ]
