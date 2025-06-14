from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null = False)
    in_stock = models.BooleanField(default=True)
   #image = models.ImageField(upload_to='images/')

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

class Brand(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()

class ProductVariant(models.Model):
    pass

class ProductReview(models.Model):
    pass

    def clean(self):
        if self.price < 0:
            return ValidationError("The price can't be negative.")

    def __str__(self):
        return self.name
    
    