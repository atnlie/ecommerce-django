from django.conf import settings
from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()

    def __self__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Item'

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __self__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'OrderItem'

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateField(auto_now_add=True)
    ordered_date = models.DateField()
    ordered = models.BooleanField(default=False)

    def __self__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Order'

