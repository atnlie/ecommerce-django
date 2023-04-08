from django.contrib import admin

from .models import Item, OrderItem, Order, BillingAddress

class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'category', 'label', 'slug', 'description']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'items', 'order_date', 'ordered']

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)