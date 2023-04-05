from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import ListView, DetailView
from .models import Item

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