# forms.py
from django import forms
from .models import VoucherClaim
import re

class VoucherClaimForm(forms.ModelForm):
    class Meta:
        model = VoucherClaim
        fields = ['full_name', 'phone_number', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama lengkap Anda',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: 0812345678901',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: nama@email.com',
                'required': True
            }),
        }
    
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        
        # Hapus semua karakter non-digit
        phone = re.sub(r'\D', '', phone)
        
        # Validasi format nomor Indonesia
        if not phone.startswith(('08', '62')):
            raise forms.ValidationError('Nomor telepon harus dimulai dengan 08 atau 62')
        
        # Standardisasi ke format 62
        if phone.startswith('08'):
            phone = '62' + phone[1:]
        
        # Validasi panjang nomor
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError('Nomor telepon tidak valid')
        
        return phone
    
    def clean_full_name(self):
        name = self.cleaned_data['full_name']
        
        # Validasi minimal 2 kata
        if len(name.split()) < 2:
            raise forms.ValidationError('Nama lengkap harus terdiri dari minimal 2 kata')
        
        # Validasi hanya huruf dan spasi
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise forms.ValidationError('Nama hanya boleh mengandung huruf dan spasi')
        
        return name.title()  # Kapitalisasi setiap kata