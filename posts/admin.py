from django.contrib import admin
from posts.models import Category, Post

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ('category', 'title', 'author', 'content', 'created_at')


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('title',)