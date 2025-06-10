# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Voucher, VoucherClaim, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['name']

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'animal_type', 
        'category',
        'location', 
        'mosque', 
        'schedule_date',
        'schedule_time',
        'total_vouchers', 
        'remaining_vouchers',
        'progress_display',
        'is_active'
    ]
    list_filter = [
        'animal_type', 
        'is_active', 
        'schedule_date',
        'category'
    ]
    search_fields = ['title', 'location', 'mosque']
    list_editable = ['is_active']
    date_hierarchy = 'schedule_date'
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage']
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('title', 'animal_type', 'category')
        }),
        ('Lokasi & Jadwal', {
            'fields': ('location', 'mosque', 'schedule_date', 'schedule_time')
        }),
        ('Voucher Management', {
            'fields': ('total_vouchers', 'remaining_vouchers', 'is_active')
        }),
        ('Informasi Sistem', {
            'fields': ('created_at', 'updated_at', 'progress_percentage'),
            'classes': ('collapse',)
        }),
    )
    
    def progress_display(self, obj):
        """Menampilkan progress bar untuk voucher"""
        percentage = obj.progress_percentage
        if percentage == 0:
            color = 'red'
        elif percentage < 50:
            color = 'orange'
        elif percentage < 80:
            color = 'yellow'
        else:
            color = 'green'
            
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0; border-radius: 3px;">'
            '<div style="width: {}%; background-color: {}; height: 20px; border-radius: 3px; text-align: center; color: white; font-size: 12px; line-height: 20px;">'
            '{}%</div></div>',
            percentage, color, int(percentage)
        )
    progress_display.short_description = 'Progress'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

@admin.register(VoucherClaim)
class VoucherClaimAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'voucher_title',
        'full_name', 
        'phone_number', 
        'email',
        'is_confirmed',
        'claimed_at'
    ]
    list_filter = [
        'is_confirmed',
        'claimed_at', 
        'voucher__animal_type',
        'voucher__category'
    ]
    search_fields = [
        'user__username', 
        'user__first_name',
        'user__last_name',
        'full_name', 
        'phone_number', 
        'email',
        'voucher__title'
    ]
    readonly_fields = ['claimed_at', 'user', 'voucher']
    list_editable = ['is_confirmed']
    date_hierarchy = 'claimed_at'
    
    fieldsets = (
        ('Informasi Klaim', {
            'fields': ('user', 'voucher', 'claimed_at', 'is_confirmed')
        }),
        ('Data Pengklaim', {
            'fields': ('full_name', 'phone_number', 'email')
        }),
        ('Catatan', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def voucher_title(self, obj):
        return obj.voucher.title
    voucher_title.short_description = 'Voucher'
    voucher_title.admin_order_field = 'voucher__title'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'voucher', 'voucher__category')

# Kustomisasi admin site
admin.site.site_header = "Berbagi Kurban Admin"
admin.site.site_title = "Berbagi Kurban"
admin.site.index_title = "Dashboard Berbagi Kurban"