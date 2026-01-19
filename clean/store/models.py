from django.db import models

class CustomerModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

class BookModel(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.title

class CartModel(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
