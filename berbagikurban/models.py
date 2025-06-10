# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nama Kategori")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Voucher(models.Model):
    ANIMAL_CHOICES = [
        ('kambing', 'Kambing'),
        ('sapi', 'Sapi'),
        ('domba', 'Domba'),
        ('kerbau', 'Kerbau'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Judul Voucher")
    animal_type = models.CharField(max_length=20, choices=ANIMAL_CHOICES, verbose_name="Jenis Hewan")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Kategori")
    location = models.CharField(max_length=200, verbose_name="Lokasi")
    mosque = models.CharField(max_length=200, verbose_name="Masjid")
    schedule_date = models.DateField(verbose_name="Tanggal Penyembelihan")
    schedule_time = models.TimeField(verbose_name="Waktu Penyembelihan")
    total_vouchers = models.IntegerField(default=0, verbose_name="Total Voucher")
    remaining_vouchers = models.IntegerField(default=0, verbose_name="Sisa Voucher")
    is_active = models.BooleanField(default=True, verbose_name="Status Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Voucher"
        verbose_name_plural = "Vouchers"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Pastikan remaining_vouchers tidak melebihi total_vouchers
        if self.remaining_vouchers > self.total_vouchers:
            self.remaining_vouchers = self.total_vouchers
        super().save(*args, **kwargs)
    
    @property
    def progress_percentage(self):
        if self.total_vouchers == 0:
            return 0
        claimed = self.total_vouchers - self.remaining_vouchers
        return round((claimed / self.total_vouchers) * 100, 2)
    
    @property
    def is_available(self):
        return self.remaining_vouchers > 0 and self.is_active
    
    @property
    def status_text(self):
        if self.remaining_vouchers == 0:
            return "HABIS"
        return f"Tersisa {self.remaining_vouchers}/{self.total_vouchers} voucher"
    
    @property
    def is_past_schedule(self):
        from datetime import datetime, time
        now = timezone.now()
        schedule_datetime = timezone.make_aware(
            datetime.combine(self.schedule_date, self.schedule_time)
        )
        return now > schedule_datetime

class VoucherClaim(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='claims')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    claimed_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, verbose_name="Nomor Telepon")
    email = models.EmailField(verbose_name="Email")
    full_name = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    is_confirmed = models.BooleanField(default=False, verbose_name="Dikonfirmasi")
    notes = models.TextField(blank=True, verbose_name="Catatan")
    
    class Meta:
        verbose_name = "Klaim Voucher"
        verbose_name_plural = "Klaim Vouchers"
        unique_together = ('voucher', 'user')  # Satu user hanya bisa klaim satu voucher yang sama
        ordering = ['-claimed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.voucher.title}"
    
    def save(self, *args, **kwargs):
        # Kurangi remaining_vouchers ketika klaim baru dibuat
        if not self.pk:  # Jika ini adalah klaim baru
            if self.voucher.remaining_vouchers > 0:
                self.voucher.remaining_vouchers -= 1
                self.voucher.save()
            else:
                raise ValueError("Voucher sudah habis!")
        super().save(*args, **kwargs)