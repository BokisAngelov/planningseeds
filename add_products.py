import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planseeds.settings')
django.setup()

from main.models import Product, Request, UserProfile

# Request.objects.all().delete()
users = UserProfile.objects.all()

print("--------------------------------")  
i =0  
for userA in users:
    # print(userA.first_name, userA.last_name, userA.email)
    print(userA.user.first_name)


# print("Products deleted successfully!")
