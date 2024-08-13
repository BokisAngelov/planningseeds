import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planseeds.settings')
django.setup()

from main.models import Product, Request

Request.objects.all().delete()

print("Products deleted successfully!")
