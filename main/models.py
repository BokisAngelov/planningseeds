from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime
from django_countries.fields import CountryField
from django.utils.translation import gettext as _
# from django.utils.translation import gettext_lazy as _lazy
# Create your models here.

class UserProfile(models.Model):

    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('producer', 'Producer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='Customer')
    id = models.UUIDField(default=uuid.uuid1, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(default=datetime.datetime.now)
    first_name = models.CharField(max_length=50, blank=False, null=True)
    last_name = models.CharField(max_length=50, blank=False, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    password = models.CharField(max_length=100, null=True, blank=False)  # Ensure to handle passwords securely
    email = models.EmailField(unique=True, blank=False, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, default="/images/default_userimg.png")
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    address = models.TextField(max_length=200, blank=True, null=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField(blank_label='Select country', null=True, blank=False)

    def __str__(self):
        return str(self.username) if self.username else str(self.id)
    
    class Meta:
        ordering = ['created']
    
    
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(null=True, blank=False) # null for db blank for django
    category = models.ManyToManyField('Categories', blank=False)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True, default="images/default_productimg.png")
    producer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'producer'}, null=True, blank=True)
    # vote_total = models.IntegerField(default=0, null=True, blank=True)
    # vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    id = models.UUIDField(default=uuid.uuid1, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['created']
    

class Review(models.Model):
    VOTE_TYPE = [
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #delete all reviews if product is deleted
    body = models.TextField(null=True, blank=True)
    value =  models.CharField(max_length=50, choices=VOTE_TYPE)
    created = models.DateTimeField(default=datetime.datetime.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value
    
    class Meta:
        ordering = ['created']
    
class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('In-progress', 'In-progress'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'customer'}, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    id = models.UUIDField(default=uuid.uuid1, unique=True, primary_key=True, editable=False)
    additional_notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['created']
    

class Offer(models.Model):
    STATUS_CHOICES = [
        ('In-progress', 'In-progress'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]

    request = models.OneToOneField(Request, on_delete=models.CASCADE, null=True, blank=True)
    producer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'producer'}, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Confirmed as decimal
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Confirmed as decimal
    delivery_timeline = models.CharField(max_length=100, blank=True, null=True)  # Confirmed as text
    additional_notes = models.TextField(blank=True, null=True)  # Confirmed as text
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In-progress')
    created = models.DateTimeField(default=datetime.datetime.now)
    id = models.UUIDField(default=uuid.uuid1, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['created']
    

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Sent', 'Sent'),
        ('Accepted', 'Accepted'),
    ]

    id = models.UUIDField(default=uuid.uuid1, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(default=datetime.datetime.now)
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE)
    invoice_file = models.FileField(upload_to='docs/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Sent')

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['created']
    
class Categories(models.Model):    
    name = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.datetime.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
