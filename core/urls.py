from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # path('', views.home, name='home'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('product/', views.product, name='product'),
    path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart')
]
