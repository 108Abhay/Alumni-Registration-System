from django.urls import path
from . import views

urlpatterns = [
    # Public URLs
    path('', views.home, name='home'),
    path('register/', views.register_alumni, name='register_alumni'),
    path('register/<uuid:token>/', views.register_alumni_with_token, name='register_alumni_with_token'),
    path('register/success/', views.register_success, name='register_success'),
    path('directory/', views.alumni_directory, name='alumni_directory'),
    path('directory/<int:alumni_id>/', views.alumni_profile_detail, name='alumni_profile_detail'),

    # Custom Admin URLs
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-approve/<int:alumni_id>/', views.approve_profile, name='approve_profile'),
    path('admin-reject/<int:alumni_id>/', views.reject_profile, name='reject_profile'),
    
    # New URL for generating registration links
    path('generate-registration-link/', views.generate_registration_link, name='generate_registration_link'),
]