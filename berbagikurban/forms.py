# berbagikurban/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import VoucherClaim, Voucher

class VoucherClaimForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan nama lengkap Anda'
        }),
        label='Nama Lengkap'
    )
    
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contoh: 08123456789'
        }),
        label='Nomor Telepon'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'contoh@email.com'
        }),
        label='Email'
    )
    
    class Meta:
        model = VoucherClaim
        fields = ['full_name', 'phone_number', 'email']