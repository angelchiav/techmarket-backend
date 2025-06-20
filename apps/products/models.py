from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return {self.name}
    

class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    needs_shipping = models.BooleanField(default=True)
    free_shipping = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    in_stock = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)
    
class RelatedProduct(models.Model):
    principal_product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    RELATIONSHIP_TYPE = [
        ('similar', 'Similar Product'),
        ('complementary', 'Complementary Good'),
        ('accessory', 'Accessory'),
        ('upgrade', 'Upgrade Version')
    ]
    relationship = models.CharField(choices=RELATIONSHIP_TYPE)

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price
    
    @property
    def discount(self):
        return self.discount_price is not None and self.discount_price < self.price
    
    @property
    def discount_percentage(self):
        if self.discount:
            return round((self.discount_price / self.price) * 100)
        return 0
    

   
    def __str__(self):
        return f'{self.name} - ${self.price}'
    