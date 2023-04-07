from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.template import loader
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.views import generic

from .forms import ContactForm, CheckoutForm
from .models import Item, OrderItem, Order


class ContactView(generic.FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_success_url(self):
        return reverse('core:contact')
    
    def form_valid(self, form):
        messages.info(self.request, 'Pesan Anda telah terkirim')
        nama = form.cleaned_data.get('nama')
        email = form.cleaned_data.get('email')
        pesan = form.cleaned_data.get('pesan')
        print(nama, email, pesan)

        full_message = f'''
            Menerima pesan berikut dari Nama: {nama} Email: {email}
            =========================================================
            
            {pesan}
        '''
        send_mail(
            subject="Menerima pesan dari website",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super(ContactView, self).form_valid(form)

class HomeView(ListView):
    model = Item
    template_name = 'index.html'

class CheckoutView(ListView):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        template_name = 'checkout.html'
        return render(self.request, template_name, context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        print(self.request.POST)
        if form.is_valid():
            print('form valid')
            return redirect('core:checkout')
        messages.warning(self.request, 'Gagal checkout')
        return redirect('core:checkout')
        # template_name = 'checkout.html'
        # return render(self.request, template_name)
        # if forms.is_valid():
        #     print('form valid')
        #     return redirect('core:checkout')
    
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'keranjang': order
            }
            template_name = 'order_summary.html'
            return render(self.request, template_name, context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Tidak ada pesanan yang aktif')
            return redirect('/')

class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'

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
            messages.info(request, 'Item sudah diupdate')
            return redirect('core:product', slug = slug)
        else:
            order.items.add(order_item)
            messages.info(request, 'Item sudah ditambahkan')
            return redirect('core:product', slug = slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'Item sudah ditambahkan')
        return redirect('core:product', slug = slug)

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
            messages.info(request, 'Item sudah dihapus')
            return redirect('core:product',slug = slug)
        else:
            # add message doest exist
            messages.info(request, 'Item tidak ada')
            return redirect('core:product',slug = slug)
    else:
        # add message
        messages.info(request, 'Item tidak ada order yang akti')
        return redirect('core:product',slug = slug)
