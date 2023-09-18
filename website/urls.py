from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.views import debug
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django/', debug.default_urlconf, name='django'),
    path('', views.landing, name='index'),
    path('autentikasi/', include('autentikasi.urls')),
    path('pengawas/', include('pengawas.urls')),
    path('petugas/', include('petugas.urls')),
    path('inven/', include('inven.urls')),
    path('test/', views.test, name='test'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
