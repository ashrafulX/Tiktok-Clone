from django.contrib import admin
from .models import Post, LikedPost, BookmarkedPost, Comment, LikedComment, Repost, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ('uuid', 'author', 'body')

@admin.register(LikedPost)
class LikedPostAdmin(admin.ModelAdmin):
    
    list_display = ('post', 'user', 'created_at')
    
@admin.register(BookmarkedPost)
class BookmarkedPostAdmin(admin.ModelAdmin):
    
    list_display = ('post', 'user', 'created_at')
    
admin.site.register(Comment)
    
@admin.register(LikedComment)
class LikedCommentAdmin(admin.ModelAdmin):
    
    list_display = ('comment', 'user', 'created_at')
    
@admin.register(Repost)
class RepostAdmin(admin.ModelAdmin):
    
    list_display = ('post', 'user', 'created_at')
    
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'count')