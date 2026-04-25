from django.contrib import admin
from .models import Post, LikedPost

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ('uuid', 'author', 'body')

@admin.register(LikedPost)
class LikedPostAdmin(admin.ModelAdmin):
    
    list_display = ('post', 'user', 'created_at')