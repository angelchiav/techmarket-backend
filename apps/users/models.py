from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom User for e-commerce"""
    email= models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    is_verified = models.BooleanField(default=False) # If the email is verified.
    accepts_marketing = models.BooleanField(default=False) # If the user accepts marketing.

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.email} - {self.get_full_name()}'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()
    
class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.email}'s profile."
    
class Address(models.Model):

    ADDRESS_TYPES =[
    ('shipping', 'Shipping'),
    ('billing', 'Billing'),
    ('both', 'Both'),
]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='shipping')

    street_address = models.CharField(max_length=200)
    apartment = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.IntegerField(blank=False)
    country = models.CharField(max_length=100)

    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    delivery_instructions = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'adresses'

    def __str__(self):
        return f'{self.street_address}, {self.city} - {self.user.email} - {self.user.full_name}'
    
class CustomerGroup(models.Model):
    """Selected group for discounts and benefits."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    min_orders = models.PositiveIntegerField(default=0) # Minimum orders to be part of.
    min_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Minimum spend to be part of.

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
"""Many to many relationship between User and Customer Group."""
User.add_to_class('customer groups', models.ManyToManyField(
    CustomerGroup,
    blank=True,
    related_name='users'
))