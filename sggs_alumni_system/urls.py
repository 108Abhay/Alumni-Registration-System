# sggs_alumni_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from alumni import views  # Import alumni views

urlpatterns = [
    path('admin/', admin.site.urls),  # Change the admin URL
    path('', include('alumni.urls')),  # Include alumni URLs first
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)