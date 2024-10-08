# Generated by Django 5.0.7 on 2024-08-05 19:30

import datetime
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_product_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='producer_name',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='vote_ratio',
        ),
        migrations.RemoveField(
            model_name='product',
            name='vote_total',
        ),
        migrations.RemoveField(
            model_name='request',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='request',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='request',
            name='requested_quantity',
        ),
        migrations.AddField(
            model_name='offer',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='offer',
            name='producer',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'producer'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userprofile'),
        ),
        migrations.AddField(
            model_name='offer',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product'),
        ),
        migrations.AddField(
            model_name='offer',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.request'),
        ),
        migrations.AddField(
            model_name='product',
            name='producer',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'producer'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userprofile'),
        ),
        migrations.AddField(
            model_name='request',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='request',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.product'),
        ),
        migrations.AddField(
            model_name='request',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='user',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'customer'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.userprofile'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('customer', 'Customer'), ('producer', 'Producer')], default='Customer', max_length=10),
        ),
        migrations.AlterField(
            model_name='offer',
            name='id',
            field=models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='offered_quantity',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='available_quantity',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='id',
            field=models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
