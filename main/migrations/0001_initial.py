# Generated by Django 5.0.7 on 2024-08-02 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('company_name', models.CharField(max_length=100)),
            ],
        ),
    ]