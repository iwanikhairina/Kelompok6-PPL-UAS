from django import forms
from .models import Voucher, Category

class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = [
            'title', 'category', 'description', 'price', 
            'total_slots', 'location', 'address', 'date', 'time', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan judul voucher'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsi voucher kambing'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Harga dalam Rupiah'
            }),
            'total_slots': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jumlah total slot tersedia',
                'min': 1
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama tempat (contoh: Masjid Jami Darussalam)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Alamat lengkap lokasi'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'title': 'Judul Voucher',
            'category': 'Kategori Hewan',
            'description': 'Deskripsi',
            'price': 'Harga (Rp)',
            'total_slots': 'Total Slot',
            'location': 'Lokasi',
            'address': 'Alamat',
            'date': 'Tanggal',
            'time': 'Waktu',
            'is_active': 'Aktif'
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Harga harus lebih besar dari 0')
        return price

    def clean_total_slots(self):
        total_slots = self.cleaned_data.get('total_slots')
        if total_slots and total_slots <= 0:
            raise forms.ValidationError('Total slot harus lebih besar dari 0')
        return total_slots


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama kategori (contoh: Kambing, Domba, Sapi)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Deskripsi kategori hewan kurban'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'name': 'Nama Kategori',
            'description': 'Deskripsi',
            'is_active': 'Aktif'
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if len(name) < 2:
                raise forms.ValidationError('Nama kategori minimal 2 karakter')
        return name