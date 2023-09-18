from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', views.index, name='login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('eror', views.eror, name='eror'),
    path('lupas_pass/', views.lupa_pass, name='lupa_pass'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
         template_name='auth/lupa_pass.html',
         html_email_template_name='auth/reset_password_email.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='auth/berhasil_kirim.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/konfirmasi_ubah.html'), name='password_reset_confirm'),
    path('reset_passworda_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='auth/berhasil_ubah.html'), name='password_reset_complete'),
]
