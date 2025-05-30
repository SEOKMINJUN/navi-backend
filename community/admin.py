from django.contrib import admin
from .models import Board, Post, Comment

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'author', 'created_at', 'view_count')
    list_filter = ('board', 'author', 'created_at')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'parent', 'created_at')
    list_filter = ('post', 'author', 'created_at')
    search_fields = ('content',)