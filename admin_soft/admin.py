from django.contrib import admin

# Register your models here.

from admin_soft.models import Product, Purchase, Sale, SaleDetail

admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(SaleDetail)