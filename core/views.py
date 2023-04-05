from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order

class HomeView(ListView):
    model = Item
    template_name = "index.html"

class CheckoutView(ListView):
    model = Item
    template_name = "checkout.html"

 #using render and we can simply pass the context and template name
def product(request):
    context = {
        'items': Item.objects.all()
    }
    template = loader.get_template('product.html')
    return HttpResponse(template.render(context, request))

# using render and we can simply pass the context and template name
def home(request):
    context = {
        'items': Item.objects.all()
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def checkout(request):
    template = loader.get_template('checkout.html')
    return HttpResponse(template.render())

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.create(item=item)
    order_query = Order.objects.filter(user=request.user, ordered=False)
    if order_query.exists():
        order = order_query[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("core:product",slug = slug)