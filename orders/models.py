from django.db import models

class Order(models.Model):
    product = models.ForeignKey(products.Product)