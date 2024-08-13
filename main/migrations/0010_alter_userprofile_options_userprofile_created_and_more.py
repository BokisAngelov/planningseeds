# Generated by Django 5.0.7 on 2024-08-06 08:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_userprofile_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ['created']},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]