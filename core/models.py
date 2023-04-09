from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATETORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATETORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()

    def __self__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "slug": self.slug
        })
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            "slug": self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            "slug": self.slug
        })
    
    class Meta:
        verbose_name_plural = 'Item'

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __self__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_harga_item(self):
        return self.quantity * self.item.price
    
    def get_total_discount_item(self):
        return self.quantity * self.item.discount_price
    
    def get_total_hemat_item(self):
        return self.get_total_harga_item() - self.get_total_discount_item()

    def get_total_item_keseluruan(self):
        if self.item.discount_price:
            return self.get_total_discount_item()
        return self.get_total_harga_item()
    
    def get_total_hemat_keseluruhan(self):
        if self.item.discount_price:
            return self.get_total_hemat_item()
        return 0
    
    class Meta:
        verbose_name_plural = 'OrderItem'

class Order(models.Model):
    trasaction_id = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateField(auto_now_add=True)
    ordered_date = models.DateField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __self__(self):
        return self.user.username
    
    def get_total_harga_order(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_keseluruan()
        return total
    
    def get_total_hemat_order(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_hemat_keseluruhan()
        return total
    class Meta:
        verbose_name_plural = 'Order'
    
class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    alamat_lokasi = models.CharField(max_length=100)
    alamat_apartemen = models.CharField(max_length=100)
    negara = CountryField(multiple=False)
    kode_pos = models.CharField(max_length=20)

    def __self__(self):
        return self.user.username
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=1)
    charge_id = models.CharField(max_length=50)

    def __self__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Payment'