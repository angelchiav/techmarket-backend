from django.db import models
from products.models import Product
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='in progress')