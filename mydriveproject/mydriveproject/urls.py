"""
URL configuration for mydriveproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from mydriveapp.views import create_google_drive_document, download_google_drive_document

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_document/', create_google_drive_document, name='create_document'),
    path('download_document/<slug:file_id>', download_google_drive_document, name='download_document'),
]
