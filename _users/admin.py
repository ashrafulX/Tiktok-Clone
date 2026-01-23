from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
            (None, {'fields': ('name', 'image', 'bio', 'birthday', 'website')}),
        ) + UserAdmin.fieldsets
    
    list_display = ('username', 'name', 'email', 'is_staff')