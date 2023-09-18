from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('petugas/', views.petugas, name='petugas'),
    path('tambah_petugas/', views.tambah_petugas, name='tambah_petugas'),
    path('hapus_petugas/<int:id>', views.hapus_petugas, name='hapus_petugas'),
    path('ubahpass/<int:id>', views.ubahpass, name='ubahpass'),

    path('barang_admin/', views.barang_admin, name='barang_admin'),
    path('d_barang/<int:id>', views.d_barang, name='d_barang'),

    path('pegawai_admin/', views.pegawai_admin, name='pegawai_admin'),
    path('d_pegawai/<int:id>', views.d_pegawai, name='d_pegawai'),

    path('lap_peminjaman/', views.lap_peminjaman, name='lap_peminjaman'),
    path('filterpinjam/', views.filterpinjam, name='filterpinjam'),

    path('lap_pengembalian/', views.lap_pengembalian, name='lap_pengembalian'),
    path('filterkembali/', views.filterkembali, name='filterkembali'),

    path('cetak_peminjaman/', views.cetak_peminjaman, name='cetak_peminjaman'),
    path('cetak_barang/', views.cetak_barang, name='cetak_barang'),
    path('cetak_pengembalian/', views.cetak_pengembalian,
         name='cetak_pengembalian'),
    path('cetak_filter_peminjaman/', views.cetak_filter_peminjaman,
         name='cetak_filter_peminjaman'),
    path('cetak_filter_pengembalian/', views.cetak_filter_pengembalian,
         name='cetak_filter_pengembalian'),

    path('cetak_barang_ex/', views.cetak_barang_ex, name='cetak_barang_ex'),
    path('cetak_pegawai_ex/', views.cetak_pegawai_ex, name='cetak_pegawai_ex'),

]
