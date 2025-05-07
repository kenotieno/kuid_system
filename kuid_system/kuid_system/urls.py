"""
URL configuration for kuid_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# kuid_system/urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from id_management import views  # Import views correctly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.search_id, name='search-id'),
    path('add/', views.add_found_id, name='add-id'),
    path('claim/<int:pk>/', views.claim_id, name='claim-id'),
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('report-lost-id/', views.report_lost_id, name='report-lost-id'),

    # Authentication
    path("register/", views.register, name="register"),  
    path("login/", views.user_login, name="login"),  
    path("logout/", views.user_logout, name="logout"),  
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
