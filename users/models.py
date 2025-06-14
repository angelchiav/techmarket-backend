from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    role = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('salesman', 'Salesman'),
        ('customer', 'Customer'),
    ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_manager(self):
        return self.role == 'manager'
    
    @property
    def is_salesman(self):
        return self.role == 'salesman'
    
    @property
    def is_customer(self):
        return self.role == 'customer'
    
    def has_role(self, *role):
        return self.role in role
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    #avatar = models.ImageField(upload_to='avatars/', null=False, blank=True)
    url = models.URLField(blank=True)



