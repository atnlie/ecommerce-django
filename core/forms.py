from django import forms
from django_countries.fields import CountryField

class ContactForm(forms.Form):
    nama = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nama Anda'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Anda'}))
    pesan = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Pesan Anda'}))


class AddressForm(forms.Form):
    pass

PILIHAN_PEMBAYARAN = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    alamat_lokasi = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Alamat Anda'}))
    alamat_apartement = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apartement, Rumah, atau yang lain (opsional)'}))
    negara = CountryField(blank_label='(Pilih Negara)').formfield()
    kode_pos = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Kode Pos'}))
    alamat_penagihan_sama = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    simpan_info_alamat = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    opsi_pembayaran = forms.ChoiceField(widget=forms.RadioSelect(), choices=PILIHAN_PEMBAYARAN)