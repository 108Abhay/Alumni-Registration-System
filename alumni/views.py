from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from .models import AlumniProfile, RegistrationLink
from .forms import AlumniRegistrationForm

def home(request):
    return render(request, 'alumni/home.html')

@csrf_protect
def register_alumni(request):
    messages.error(request, 'Direct registration is not allowed. Please use the provided registration link.')
    return redirect('home')

def register_success(request):
    return render(request, 'alumni/register_success.html')

def alumni_directory(request):
    approved_alumni = AlumniProfile.objects.filter(status='Approved')
    return render(request, 'alumni/directory.html', {'alumni': approved_alumni})

def alumni_profile_detail(request, alumni_id):
    alumni = get_object_or_404(AlumniProfile, id=alumni_id, status='Approved')
    return render(request, 'alumni/profile_detail.html', {'alumni': alumni})

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser, login_url='/admin-login/')
def generate_registration_link(request):
    # Create a new registration link for the current admin
    link = RegistrationLink.objects.create(created_by=request.user)
    
    # Generate the full registration URL
    registration_url = request.build_absolute_uri(
        reverse('register_alumni_with_token', kwargs={'token': link.token})
    )
    
    return render(request, 'alumni/registration_link.html', {
        'registration_url': registration_url
    })

def register_alumni_with_token(request, token):
    try:
        reg_link = RegistrationLink.objects.get(token=token, is_active=True)
        if (timezone.now() - reg_link.created_at).days > 7:
            messages.error(request, 'Registration link has expired.')
            return redirect('home')
        
        if request.method == 'POST':
            form = AlumniRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.registration_link = reg_link
                profile.save()
                
                reg_link.is_active = False
                reg_link.used_at = timezone.now()
                reg_link.save()
                
                return redirect('register_success')
        else:
            form = AlumniRegistrationForm()
        
        return render(request, 'alumni/register.html', {
            'form': form, 
            'token_valid': True
        })
    
    except RegistrationLink.DoesNotExist:
        messages.error(request, 'Invalid registration link.')
        return redirect('home')

@user_passes_test(is_superuser, login_url='/admin-login/')
def admin_dashboard(request):
    pending_profiles = AlumniProfile.objects.filter(status='Pending')
    return render(request, 'alumni/admin_dashboard.html', {'profiles': pending_profiles})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized.')
    
    return render(request, 'alumni/admin_login.html')

def admin_logout(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('home')

@user_passes_test(is_superuser, login_url='/admin-login/')
def approve_profile(request, alumni_id):
    alumni = get_object_or_404(AlumniProfile, id=alumni_id)
    alumni.status = 'Approved'
    alumni.save()
    messages.success(request, 'Profile approved successfully.')
    return redirect('admin_dashboard')

@user_passes_test(is_superuser, login_url='/admin-login/')
def reject_profile(request, alumni_id):
    alumni = get_object_or_404(AlumniProfile, id=alumni_id)
    alumni.status = 'Rejected'
    alumni.save()
    messages.success(request, 'Profile rejected successfully.')
    return redirect('admin_dashboard')
