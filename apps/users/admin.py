from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
        ('Additional info', {
            'fields': ('phone', 'birth_date', 'is_verified')
        })
    

        add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional info', {
            'fields': ('email', 'phone', 'birth_date')
        })
    )