from django.contrib import admin

from .models import Item, OrderItem, Order, Address, Payment

class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'category', 'label', 'slug', 'description']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'trasaction_id', 'ordered_date', 'ordered', 'payment', 'billing_address', 'shipping_address']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'quantity']

# class AddressAdmin(admin.ModelAdmin):
#     list_display = ['user','alamat_lokasi','alamat_lokasi','alamat_apartemen','negara','kode_pos', 'tipe_alamat', 'default']
#     list_filter = ['default', 'tipe_alamat', 'negara']
#     search_fields = ['user', 'alamat_lokasi', 'alamat_apartemen', 'kode_pos']

class AddressAdminV2(admin.ModelAdmin):
    list_display = ['user','alamat_lokasi','alamat_lokasi','alamat_apartemen','negara','kode_pos', 'tipe_alamat', 'default']
    list_filter = ['default', 'tipe_alamat', 'negara']
    search_fields = ['user', 'alamat_lokasi', 'alamat_apartemen', 'kode_pos']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'timestamp', 'payment_option', 'charge_id']

admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(Address, AddressAdmin)
admin.site.register(Address, AddressAdminV2)
admin.site.register(Payment, PaymentAdmin)