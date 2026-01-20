from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'price', 'stock', 'category', 'created_at']
    search_fields = ['title', 'author', 'isbn', 'category']
    list_filter = ['category', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['stock', 'price']
