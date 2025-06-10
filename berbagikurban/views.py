# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
from .models import Voucher, VoucherClaim
from .forms import VoucherClaimForm

def splashscreen(request):
    return render(request, 'splash.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username atau password salah!')
    
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        print("POST request received")  # Debug print
        
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        email = request.POST.get('email', '').strip()
        
        print(f"Data received - Username: {username}, Email: {email}")  # Debug print
        
        # Validasi input kosong
        if not username:
            messages.error(request, 'Username harus diisi!')
            return render(request, 'signup.html')
        
        if not password:
            messages.error(request, 'Password harus diisi!')
            return render(request, 'signup.html')
        
        if not confirm_password:
            messages.error(request, 'Konfirmasi password harus diisi!')
            return render(request, 'signup.html')
        
        # Validasi password match
        if password != confirm_password:
            messages.error(request, 'Password dan konfirmasi password tidak sama!')
            return render(request, 'signup.html')
        
        # Validasi panjang password
        if len(password) < 6:
            messages.error(request, 'Password minimal 6 karakter!')
            return render(request, 'signup.html')
        
        # Cek apakah username sudah ada
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan!')
            return render(request, 'signup.html')
        
        # Cek apakah email sudah ada (jika email diisi)
        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan!')
            return render(request, 'signup.html')
        
        try:
            # Buat user baru
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email if email else ''
            )
            print(f"User created successfully: {user.username}")  # Debug print
            messages.success(request, 'Akun berhasil dibuat! Silakan login.')
            
            # Redirect ke login
            return redirect('login')
                
        except IntegrityError as e:
            print(f"IntegrityError: {e}")  # Debug print
            messages.error(request, 'Username atau email sudah digunakan!')
            return render(request, 'signup.html')
        except Exception as e:
            print(f"Exception: {e}")  # Debug print
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')

@login_required
def home_view(request):
    # Ambil semua voucher yang aktif
    vouchers = Voucher.objects.filter(is_active=True).order_by('-created_at')
    
    # Cek voucher yang sudah diklaim user
    user_claims = VoucherClaim.objects.filter(user=request.user)
    claimed_voucher_ids = user_claims.values_list('voucher_id', flat=True)
    
    # Filter berdasarkan jenis hewan jika ada
    animal_filter = request.GET.get('jenis')
    if animal_filter:
        vouchers = vouchers.filter(animal_type=animal_filter)
    
    # Search berdasarkan judul atau lokasi
    search_query = request.GET.get('search')
    if search_query:
        vouchers = vouchers.filter(
            models.Q(title__icontains=search_query) |
            models.Q(location__icontains=search_query) |
            models.Q(mosque__icontains=search_query)
        )
    
    context = {
        'vouchers': vouchers,
        'user_claims': user_claims,
        'claimed_voucher_ids': claimed_voucher_ids,
        'has_claims': user_claims.exists(),
        'animal_choices': Voucher.ANIMAL_CHOICES,
        'current_filter': animal_filter,
        'current_search': search_query
    }
    return render(request, 'home.html', context)

@login_required
def voucher_detail(request, voucher_id):
    # Ambil voucher berdasarkan ID
    voucher = get_object_or_404(Voucher, id=voucher_id, is_active=True)
    
    # Cek apakah user sudah pernah klaim voucher ini
    existing_claim = VoucherClaim.objects.filter(user=request.user, voucher=voucher).first()
    
    context = {
        'voucher': voucher,
        'existing_claim': existing_claim,
        'already_claimed': existing_claim is not None,
        'can_claim': voucher.is_available and not existing_claim
    }
    return render(request, 'voucher_detail.html', context)

@login_required
def klaim_voucher(request, voucher_id):
    # Ambil voucher berdasarkan ID
    voucher = get_object_or_404(Voucher, id=voucher_id, is_active=True)
    
    # Cek apakah voucher masih tersedia
    if not voucher.is_available:
        messages.error(request, 'Voucher sudah habis atau tidak aktif.')
        return redirect('voucher_detail', voucher_id=voucher_id)
    
    # Cek apakah user sudah pernah klaim voucher ini
    existing_claim = VoucherClaim.objects.filter(user=request.user, voucher=voucher).first()
    
    if existing_claim:
        messages.info(request, 'Anda sudah pernah mengklaim voucher ini.')
        return redirect('voucher_detail', voucher_id=voucher_id)
    
    if request.method == 'POST':
        form = VoucherClaimForm(request.POST)
        if form.is_valid():
            try:
                # Simpan data ke database dengan transaksi
                with transaction.atomic():
                    # Cek lagi apakah voucher masih tersedia (double check)
                    voucher.refresh_from_db()
                    if not voucher.is_available:
                        messages.error(request, 'Voucher sudah habis saat Anda mengisi form.')
                        return render(request, 'klaim_voucher.html', {'form': form, 'voucher': voucher})
                    
                    # Simpan klaim voucher
                    voucher_claim = form.save(commit=False)
                    voucher_claim.user = request.user
                    voucher_claim.voucher = voucher
                    voucher_claim.save()
                    
                    # Kurangi sisa voucher
                    voucher.remaining_vouchers -= 1
                    voucher.save()
                
                messages.success(request, 'Klaim voucher berhasil disimpan!')
                return redirect('voucher_success', voucher_id=voucher_id)
                
            except IntegrityError:
                messages.error(request, 'Anda sudah pernah mengklaim voucher ini.')
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan: {str(e)}')
    else:
        form = VoucherClaimForm()
    
    context = {
        'form': form,
        'voucher': voucher
    }
    return render(request, 'klaim_voucher.html', context)

@login_required
def voucher_success(request, voucher_id):
    # Ambil voucher dan klaim yang baru saja dibuat
    voucher = get_object_or_404(Voucher, id=voucher_id)
    claim = get_object_or_404(VoucherClaim, user=request.user, voucher=voucher)
    
    context = {
        'claim': claim,
        'voucher': voucher
    }
    return render(request, 'voucher_success.html', context)

def logout_view(request):
    logout(request)
    return redirect('splash')