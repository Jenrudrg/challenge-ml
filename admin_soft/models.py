from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Products
class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_created_user')
    modifier_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_modifier_user')
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

# Purchases
class Purchase(models.Model):
    uuid = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_created_user')
    modifier_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_modifier_user')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.uuid)

class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_detail')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-id']

    def calculate_total_price_purchase(self):
        return self.purchase_price * self.quantity

    def __str__(self):
        return str(self.purchase.uuid)


# Sales
class Sale(models.Model):
    uuid = models.UUIDField(unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sale_created_user')
    modifier_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sale_modifier_user')
    date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.uuid)

# Sales Details
class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_detail')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        ordering = ['-id']

    def calculate_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.sale.uuid)