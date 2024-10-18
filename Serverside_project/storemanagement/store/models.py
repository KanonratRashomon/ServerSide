from django.db import models
from django.contrib.auth.models import User
# class Customer(models.Model):
#     first_name = models.CharField(max_length=150, null=False)
#     last_name = models.CharField(max_length=200, null=False)
#     email = models.CharField(max_length=150, null=False)
#     address = models.JSONField(null=True)

#     def __str__(self):
#         return self.username

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class Products(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    product_category = models.ManyToManyField("store.Category")
    price = models.FloatField()
    discount = models.FloatField(default=0)
    stock_quantity = models.IntegerField(default=0)
    release_date = models.DateField()
    product_image = models.ImageField(null=True, blank=True, upload_to="images/")
    added_by_employee = models.ForeignKey('Employee', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_discounted_price(self):
        if self.discount > 0:
            discount_amount = (self.discount / 100) * self.price
            return self.price - discount_amount
        return self.price

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.title} ({self.quantity})'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items', null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f'{self.product.title} - {self.quantity}'