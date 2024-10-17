from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=150, null=False)
    address = models.JSONField(null=True)

    def __str__(self):
        return self.username

class Orders(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"

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
    order = models.ForeignKey(Orders, on_delete=models.CASCADE) #อ้างอิงจาก Orders
    product = models.ForeignKey(Products, on_delete=models.CASCADE) #อ้างอิงจาก Products
    quantity = models.IntegerField()
    unit_price = models.FloatField()

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Order {self.order.id}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
