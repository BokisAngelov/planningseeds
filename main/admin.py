from django.contrib import admin
from .models import UserProfile, Product, Review, Categories

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Categories)
