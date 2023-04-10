from uuid import uuid4
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.template import loader
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from django.views import generic
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED

from .forms import ContactForm, CheckoutForm, CheckoutFormV2
from .models import Item, OrderItem, Order, Address, Payment


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

class PaymentView(generic.FormView):
    def get(self, *args, **kwargs):
        template_name = 'payment.html'
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.trasaction_id == '':
                order.trasaction_id = str(uuid4())
                order.save()
            
            paypal_data = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': order.get_total_harga_order,
                'item_name': f'Pembayaran belajanan order: {order.trasaction_id}',
                'invoice': order.trasaction_id,
                'currency_code': 'USD',
                'notify_url': self.request.build_absolute_uri(reverse('paypal-ipn')),
                'return_url': self.request.build_absolute_uri(reverse('core:paypal-return')),
                'cancel_return': self.request.build_absolute_uri(reverse('core:paypal-cancel')),
            }
        
            qPath = self.request.get_full_path()
            isPaypal = 'paypal' in qPath
        
            form = PayPalPaymentsForm(initial=paypal_data)
            context = {
                'paypalform': form,
                'order': order,
                'is_paypal': isPaypal,
            }
            return render(self.request, template_name, context)

        except ObjectDoesNotExist:
            return redirect('core:checkout')

@csrf_exempt
def paypal_return(request):
    # update oder status
    print(request)
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order.payment = payment
        order.ordered = True
        order.save()
    
        payment = Payment()
        payment.user=request.user
        payment.amount = order.get_total_harga_order
        payment.payment_option = 'P' # paypal
        payment.charge_id = f'{uuid4()}-{timezone.now()}'
        payment.timestamp = timezone.now()
        payment.save()

    except ObjectDoesNotExist:
        messages.error(request, 'Pembayaran sudah diterima, tapi tidak bisa disimpan')

    try:
        order_item = OrderItem.objects.filter(user=request.user,ordered=False)

        for item in order_item:
            item.ordered = True
            item.save()
    except ObjectDoesNotExist:
        messages.error(request, 'Pembayaran sudah diterima, tapi tidak bisa update order item')


    messages.error(request, 'Pembayaran sudah diterima, terima kasih')
    return redirect('core:home')

@csrf_exempt
def paypal_cancel(request):
    messages.error(request, 'Pembayaran dibatalkan')
    return redirect('core:order-summary')


class CheckoutView(ListView):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.items.count() == 0:
                messages.warning(self.request, 'Belum ada belajaan yang Anda pesan, lanjutkan belanja')
                return redirect('core:home')
        except ObjectDoesNotExist:
            order = {}
            messages.warning(self.request, 'Belum ada belajaan yang Anda pesan, lanjutkan belanja')
            return redirect('core:home')

        context = {
            'form': form,
            'order': order,
        }
        template_name = 'checkout.html'
        return render(self.request, template_name, context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                alamat_lokasi = form.cleaned_data.get('alamat_lokasi')
                alamat_apartemen = form.cleaned_data.get('alamat_apartemen')
                negara = form.cleaned_data.get('negara')
                kode_pos = form.cleaned_data.get('kode_pos')
                # TODO: membutuhkan logic simpan dan menggunakan alamat yang sama
                # alamat_penagihan_sama = form.cleaned_data.get('alamat_penagihan_sama')
                # simpan_info_alamat = form.cleaned_data.get('simpan_info_alamat')
                opsi_pembayaran = form.cleaned_data.get('opsi_pembayaran')
                alamat_billing = Address(
                    user=self.request.user,
                    alamat_lokasi=alamat_lokasi,
                    alamat_apartemen=alamat_apartemen,
                    negara=negara,
                    kode_pos=kode_pos,
                    tipe_alamat='B',
                )
                alamat_billing.save()
                order.billing_address = alamat_billing
                order.tranasction_id = str(uuid4())
                order.save()
                if opsi_pembayaran == 'P':
                    return redirect('core:payment', payment_method='paypal')
                else:
                    messages.warning(self.request, 'Gunakan Paypal saja ya')
                    return redirect('core:payment', payment_method='stripe')

            messages.warning(self.request, 'Gagal checkout')
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Tidak ada pesanan yang aktif')
            return redirect('core:order-summary')

class CheckoutViewV2(ListView):
    def get(self, *args, **kwargs):
        form = CheckoutFormV2()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if order.items.count() == 0:
                messages.warning(self.request, 'Belum ada belajaan yang Anda pesan, lanjutkan belanja')
                return redirect('core:home')
            context = {
                'form': form,
                'order': order,
            }
            
            query_alamat_pengiriman = Address.objects.filter(
                user=self.request.user,
                tipe_alamat='S',
                default=True
            )
            if query_alamat_pengiriman.exists():
                context.update(
                    {'default_shipping_address': query_alamat_pengiriman[0]})

            query_alamat_penagihan = Address.objects.filter(
                user=self.request.user,
                tipe_alamat='B',
                default=True
            )
            if query_alamat_penagihan.exists():
                context.update(
                    {'default_billing_address': query_alamat_penagihan[0]})
            
            template_name = 'checkout_v2.html'
            return render(self.request, template_name, context)
        except ObjectDoesNotExist:
            order = {}
            messages.warning(self.request, 'Belum ada belajaan yang Anda pesan, lanjutkan belanja')
            return redirect('core:home')

    def post(self, *args, **kwargs):
        form = CheckoutFormV2(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                print('Masuk valid ga?')
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("menggunakan alamat default pengiriman")
                    query_alamat = Address.objects.filter(
                        user=self.request.user,
                        tipe_alamat='S',
                        default=True
                    )
                    if query_alamat.exists():
                        alamat_pengiriman = query_alamat[0]
                        order.shipping_address = alamat_pengiriman
                        order.save()
                    else:
                        messages.info(self.request, "Tidak ada alamat pengiriman yang tersedia")
                        return redirect('core:checkout-v2')
                else:
                    print("Menggunakan alamat pengiriman baru")
                    alamat_pengiriman1 = form.cleaned_data.get(
                        'alamat_pengiriman')
                    alamat_pengiriman2 = form.cleaned_data.get(
                        'alamat_pengiriman2')
                    negara_pengiriman = form.cleaned_data.get(
                        'negara_pengiriman')
                    kodepos_pengiriman = form.cleaned_data.get('kodepos_pengiriman')

                    if is_form_valid([alamat_pengiriman1, negara_pengiriman, kodepos_pengiriman]):
                        alamat_pengiriman = Address(
                            user=self.request.user,
                            alamat_lokasi=alamat_pengiriman1,
                            alamat_apartemen=alamat_pengiriman2,
                            negara=negara_pengiriman,
                            kode_pos=kodepos_pengiriman,
                            tipe_alamat='S'
                        )
                        alamat_pengiriman.save()

                        order.shipping_address = alamat_pengiriman
                        order.save()

                        set_default_pengiriman = form.cleaned_data.get(
                            'set_default_pengiriman')
                        if set_default_pengiriman:
                            alamat_pengiriman.default = True
                            alamat_pengiriman.save()

                    else:
                        messages.info(self.request, "Isi alamat pengiriman dengan benar")
                
                use_default_penagihan = form.cleaned_data.get(
                    'use_default_penagihan')
                sama_alamat_penagihan = form.cleaned_data.get(
                    'sama_alamat_penagihan')
                
                if sama_alamat_penagihan:
                    alamat_penagihan = alamat_pengiriman
                    alamat_penagihan.pk = None
                    # alamat_penagihan.save()
                    alamat_penagihan.tipe_alamat = 'B'
                    alamat_penagihan.save()
                    order.billing_address = alamat_penagihan
                    order.save()
                elif use_default_penagihan:
                    print("Menggunakan alamat default penagihan")
                    query_alamat = Address.objects.filter(
                        user=self.request.user,
                        tipe_alamat ='B',
                        default = True
                    )
                    if query_alamat.exists():
                        alamat_penagihan = query_alamat[0]
                        order.billing_address = alamat_penagihan
                        order.save()
                    else:
                        messages.info(self.request, "Tidak ada default alamat penagihan yang tersedia")
                        return redirect('core:checkout-v2')
                else:
                    print("Input alamat penagihan baru")
                    alamat_penagihan1 = form.cleaned_data.get(
                        'alamat_penagihan')
                    alamat_penagihan2 = form.cleaned_data.get(
                        'alamat_penagiha2')
                    negara_penagihan = form.cleaned_data.get(
                        'negara_penagihan')
                    kodepos_penagihan = form.cleaned_data.get('kodepos_penagihan')

                    if is_form_valid([alamat_penagihan1, negara_penagihan, kodepos_penagihan]):
                        alamat_penagihan = Address(
                            user=self.request.user,
                            alamat_lokasi=alamat_penagihan1,
                            alamat_apartemen=alamat_penagihan2,
                            negara=negara_penagihan,
                            kode_pos=kodepos_penagihan,
                            tipe_alamat='B'
                        )
                        alamat_penagihan.save()

                        order.billing_address = alamat_penagihan
                        order.save()

                        set_default_penagihan = form.cleaned_data.get(
                            'set_default_penagihan')
                        if set_default_penagihan:
                            alamat_penagihan.default = True
                            alamat_penagihan.save()
                    else:
                        messages.info(self.request, "Isi alamat penagihan dengan benar")
                
                opsi_pembayaran = form.cleaned_data.get('opsi_pembayaran')

                if opsi_pembayaran == 'S':
                    return redirect('core:payment', payment_method='stripe')
                elif opsi_pembayaran == 'P':
                    return redirect('core:payment', payment_method='paypal')
                else:
                    messages.warning(self.request, "Opsi pembayaran tidak tersedia")
                    return redirect('core:checkout-v2')
                
                # alamat_lokasi = form.cleaned_data.get('alamat_lokasi')
                # alamat_apartemen = form.cleaned_data.get('alamat_apartemen')
                # negara = form.cleaned_data.get('negara')
                # kode_pos = form.cleaned_data.get('kode_pos')
                # # TODO: membutuhkan logic simpan dan menggunakan alamat yang sama
                # # alamat_penagihan_sama = form.cleaned_data.get('alamat_penagihan_sama')
                # # simpan_info_alamat = form.cleaned_data.get('simpan_info_alamat')
                # opsi_pembayaran = form.cleaned_data.get('opsi_pembayaran')
                # alamat_billing = Address(
                #     user=self.request.user,
                #     alamat_lokasi=alamat_lokasi,
                #     alamat_apartemen=alamat_apartemen,
                #     negara=negara,
                #     kode_pos=kode_pos,
                #     tipe_alamat='B',
                # )
                # alamat_billing.save()
                # order.billing_address = alamat_billing
                # order.tranasction_id = str(uuid4())
                # order.save()
                # if opsi_pembayaran == 'P':
                #     return redirect('core:payment', payment_method='paypal')
                # else:
                #     messages.warning(self.request, 'Gunakan Paypal saja ya')
                #     return redirect('core:payment', payment_method='stripe')

            messages.warning(self.request, 'Gagal checkout')
            return redirect('core:checkout-v2')
        except ObjectDoesNotExist:
            messages.error(self.request, 'Tidak ada pesanan yang aktif')
            return redirect('core:order-summary')


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
           try: 
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]
                order.items.remove(order_item)
                # add message
                messages.info(request, 'Item sudah dihapus')
                return redirect('core:product',slug = slug)
           except ObjectDoesNotExist:
               print('Error: order item sudah tidak ada')
        else:
            # add message doest exist
            messages.info(request, 'Item tidak ada')
            return redirect('core:product',slug = slug)
    else:
        # add message
        messages.info(request, 'Item tidak ada order yang akti')
        return redirect('core:product',slug = slug)

def is_form_valid(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid