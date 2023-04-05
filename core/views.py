from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import generic

class HomeView(generic.TemplateView):
    template_name = "index.html"

class CheckoutView(generic.TemplateView):
    template_name = "checkout.html"

def product(request):
    template = loader.get_template('product.html')
    return HttpResponse(template.render())