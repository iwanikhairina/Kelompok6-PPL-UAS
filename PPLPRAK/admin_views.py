from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Voucher, Category
from .admin_forms import VoucherForm, CategoryForm

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_vouchers = Voucher.objects.count()
    active_vouchers = Voucher.objects.filter(is_active=True).count()
    total_categories = Category.objects.count()
    total_slots = sum(voucher.total_slots for voucher in Voucher.objects.all())
    available_slots = sum(voucher.available_slots for voucher in Voucher.objects.all())
    
    recent_vouchers = Voucher.objects.order_by('-created_at')[:5]
    
    context = {
        'total_vouchers': total_vouchers,
        'active_vouchers': active_vouchers,
        'total_categories': total_categories,
        'total_slots': total_slots,
        'available_slots': available_slots,
        'recent_vouchers': recent_vouchers,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def voucher_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    
    vouchers = Voucher.objects.all()
    
    if search_query:
        vouchers = vouchers.filter(
            Q(title__icontains=search_query) | 
            Q(location__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_filter:
        vouchers = vouchers.filter(category_id=category_filter)
    
    if status_filter:
        if status_filter == 'active':
            vouchers = vouchers.filter(is_active=True)
        elif status_filter == 'inactive':
            vouchers = vouchers.filter(is_active=False)
    
    vouchers = vouchers.order_by('-created_at')
    
    paginator = Paginator(vouchers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'categories': categories,
    }
    return render(request, 'admin/voucher_list.html', context)

@login_required
@user_passes_test(is_admin)
def voucher_create(request):
    if request.method == 'POST':
        form = VoucherForm(request.POST, request.FILES)
        if form.is_valid():
            voucher = form.save(commit=False)
            voucher.available_slots = voucher.total_slots
            voucher.save()
            messages.success(request, 'Voucher berhasil dibuat!')
            return redirect('admin:voucher_list')
    else:
        form = VoucherForm()
    
    return render(request, 'admin/voucher_form.html', {
        'form': form,
        'title': 'Tambah Voucher Baru'
    })

@login_required
@user_passes_test(is_admin)
def voucher_edit(request, pk):
    voucher = get_object_or_404(Voucher, pk=pk)
    
    if request.method == 'POST':
        form = VoucherForm(request.POST, request.FILES, instance=voucher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Voucher berhasil diperbarui!')
            return redirect('admin:voucher_list')
    else:
        form = VoucherForm(instance=voucher)
    
    return render(request, 'admin/voucher_form.html', {
        'form': form,
        'title': 'Edit Voucher',
        'voucher': voucher
    })

@login_required
@user_passes_test(is_admin)
def voucher_delete(request, pk):
    voucher = get_object_or_404(Voucher, pk=pk)
    
    if request.method == 'POST':
        voucher.delete()
        messages.success(request, 'Voucher berhasil dihapus!')
        return redirect('admin:voucher_list')
    
    return render(request, 'admin/voucher_delete.html', {
        'voucher': voucher
    })

@login_required
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'admin/category_list.html', {
        'categories': categories
    })

@login_required
@user_passes_test(is_admin)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori berhasil dibuat!')
            return redirect('admin:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'admin/category_form.html', {
        'form': form,
        'title': 'Tambah Kategori Baru'
    })

@login_required
@user_passes_test(is_admin)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori berhasil diperbarui!')
            return redirect('admin:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/category_form.html', {
        'form': form,
        'title': 'Edit Kategori',
        'category': category
    })

@login_required
@user_passes_test(is_admin)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori berhasil dihapus!')
        return redirect('admin:category_list')
    
    return render(request, 'admin/category_delete.html', {
        'category': category
    })