from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model"""
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'price', 'isbn', 
                  'stock', 'category', 'image_url', 'in_stock', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_in_stock(self, obj):
        """Return whether book is in stock"""
        return obj.is_in_stock()


class BookListSerializer(serializers.ModelSerializer):
    """Lighter serializer for book list (without full description)"""
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'isbn', 
                  'stock', 'category', 'image_url', 'in_stock']

    def get_in_stock(self, obj):
        return obj.is_in_stock()


class BookCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new books"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'price', 'isbn', 
                  'stock', 'category', 'image_url']

    def validate_price(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_stock(self, value):
        """Ensure stock is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value
