from django.contrib import admin
from .models import Post, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'updated_at')
    search_fields = ('content', 'author__username', 'post__title')
    list_filter = ('created_at',)
