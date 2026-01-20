from django.db import models


class Book(models.Model):
    """Book model for catalog management"""
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=13, unique=True)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_in_stock(self):
        """Check if book is available in stock"""
        return self.stock > 0

    def has_sufficient_stock(self, quantity):
        """Check if there's sufficient stock for the requested quantity"""
        return self.stock >= quantity
