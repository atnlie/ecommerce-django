from django.urls import path
from . import views

from core import views
app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('', views.home, name='home'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('product/', views.product, name='product'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('payment', views.PaymentView.as_view(), name='payment'),
    # path('payment/<payment_method>', views.PaymentView.as_view(), name='payment'),
    
]
