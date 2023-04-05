from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('product/', views.product, name='product'),
]
