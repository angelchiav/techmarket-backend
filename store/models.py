from django.db import models
import datetime

# Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

 # Costumers
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email =  models.EmailField(primary_key=True, max_length=100)
    password = models.CharField(max_length=150)
    password2 = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Products
class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=250, default='', null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='uploads/products/')

    def __str__(self):
        return self.name

# Customer Orders
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=False)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product