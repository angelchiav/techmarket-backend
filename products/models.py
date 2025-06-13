from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null = False)
    in_stock = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    