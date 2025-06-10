# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Voucher(models.Model):
    ANIMAL_CHOICES = [
        ('kambing', 'Kambing'),
        ('sapi', 'Sapi'),
        ('domba', 'Domba'),
        ('kerbau', 'Kerbau'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Judul Voucher")
    animal_type = models.CharField(max_length=20, choices=ANIMAL_CHOICES, verbose_name="Jenis Hewan")
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
    
    @property
    def progress_percentage(self):
        if self.total_vouchers == 0:
            return 0
        claimed = self.total_vouchers - self.remaining_vouchers
        return (claimed / self.total_vouchers) * 100
    
    @property
    def is_available(self):
        return self.remaining_vouchers > 0 and self.is_active
    
    @property
    def status_text(self):
        if self.remaining_vouchers == 0:
            return "HABIS"
        return f"Tersisa {self.remaining_vouchers}/{self.total_vouchers} voucher"

class VoucherClaim(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='claims')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    claimed_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, verbose_name="Nomor Telepon")
    email = models.EmailField(verbose_name="Email")
    full_name = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    
    class Meta:
        verbose_name = "Klaim Voucher"
        verbose_name_plural = "Klaim Vouchers"
        unique_together = ('voucher', 'user')  # Satu user hanya bisa klaim satu voucher yang sama
    
    def __str__(self):
        return f"{self.user.username} - {self.voucher.title}"