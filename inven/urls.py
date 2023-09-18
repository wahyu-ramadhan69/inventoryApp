from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('json/', views.json, name='json')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
