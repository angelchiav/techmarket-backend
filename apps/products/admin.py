from django.contrib import admin
from .models import Category, Product, RelatedProduct

admin.register.site(Product)
admin.register.site(Category)
admin.register.site(RelatedProduct)