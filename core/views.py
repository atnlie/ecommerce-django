from django.http import HttpResponse
from django.contrib import messages
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
    order_item, _ = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_query = Order.objects.filter(user=request.user, ordered=False)
    if order_query.exists():
        order = order_query[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item sudah diupdate")
            return redirect("core:product", slug = slug)
        else:
            order.items.add(order_item)
            messages.info(request, "Item sudah ditambahkan")
            return redirect("core:product", slug = slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item sudah ditambahkan")
        return redirect("core:product", slug = slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_query = Order.objects.filter(
        user=request.user, ordered=False
    )
    if order_query.exists():
        order = order_query[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            # add message
            messages.info(request, "Item sudah dihapus")
            return redirect("core:product",slug = slug)
        else:
            # add message doest exist
            messages.info(request, "Item tidak ada")
            return redirect("core:product",slug = slug)
    else:
        # add message
        messages.info(request, "Item tidak ada order yang aktif")
        return redirect("core:product",slug = slug)