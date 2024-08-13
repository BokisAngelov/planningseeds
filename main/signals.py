from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth.models import User

# @receiver(post_save, sender=UserProfile)
def createProfile(sender, instance, created, **kwargs):
    if created == True:
        user = instance
        user_type = getattr(user, 'user_type', 'customer')
        profile = UserProfile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            first_name=user.first_name,
            user_type = user_type,
        )

# @receiver(post_delete, sender=UserProfile)
def profileDelete(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    
post_save.connect(createProfile, sender=User)
post_delete.connect(profileDelete, sender=UserProfile)