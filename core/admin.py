from django.contrib import admin

from .models import Item, OrderItem, Order, BillingAddress, Payment

class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'category', 'label', 'slug', 'description']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'trasaction_id', 'ordered_date', 'ordered', 'payment', 'billing_address']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'quantity']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','alamat_lokasi','alamat_lokasi','alamat_apartemen','negara','kode_pos']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'timestamp', 'payment_option', 'charge_id']

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(BillingAddress, AddressAdmin)
admin.site.register(Payment, PaymentAdmin)