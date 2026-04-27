from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
            (None, {'fields': ('name', 'image', 'bio', 'birthday', 'website')}),
        ) + UserAdmin.fieldsets
    
    list_display = ('username', 'name', 'email', 'is_staff', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image"