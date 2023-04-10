from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

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
    alamat_lokasi = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Alamat Anda', 'class': 'textinput form-control'}))
    alamat_apartemen = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apartement, Rumah, atau yang lain (opsional)', 'class': 'textinput form-control'}))
    negara = CountryField(blank_label='(Pilih Negara)').formfield(widget=CountrySelectWidget(attrs={'class': 'countryselectwidget form-select'}))
    kode_pos = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Kode Pos', 'class': 'form-control'}))
    alamat_penagihan_sama = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    simpan_info_alamat = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    opsi_pembayaran = forms.ChoiceField(widget=forms.RadioSelect(), choices=PILIHAN_PEMBAYARAN)


class CheckoutFormV2(forms.Form):
    alamat_pengiriman = forms.CharField(required=False)
    alamat_pengiriman2 = forms.CharField(required=False)
    negara_pengiriman = CountryField(blank_label='(pilih negara)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'countryselectwidget form-select',
        }))
    kodepos_pengiriman = forms.CharField(required=False)

    alamat_penagihan = forms.CharField(required=False)
    alamat_penagihan2 = forms.CharField(required=False)
    negara_penagihan = CountryField(blank_label='(pilih negara)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'countryselectwidget form-select',
        }))
    kodepos_penagihan = forms.CharField(required=False)

    sama_alamat_penagihan = forms.BooleanField(required=False)
    set_default_pengiriman = forms.BooleanField(required=False)
    use_default_pengiriman = forms.BooleanField(required=False)
    set_default_penagihan = forms.BooleanField(required=False)
    use_default_penagihan = forms.BooleanField(required=False)

    opsi_pembayaran = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PILIHAN_PEMBAYARAN)