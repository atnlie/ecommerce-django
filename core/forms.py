from django import forms

class ContactForm(forms.Form):
    nama = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nama Anda'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Anda'}))
    pesan = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Pesan Anda'}))