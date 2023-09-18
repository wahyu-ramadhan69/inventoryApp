from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.dashboard_op, name='dashboard_op'),

    path('pegawai_op/', views.pegawai_op, name='pegawai_op'),
    path('tambahpegawai/', views.tambahpegawai, name='tambahpegawai'),
    path('detail_pegawai/<int:id>', views.detail_pegawai, name='detail_pegawai'),
    path('edit_pegawai/<int:id>', views.edit_pegawai, name='edit_pegawai'),
    path('hapus_pegawai/<int:id>', views.hapus_pegawai, name='hapus_pegawai'),

    path('barang_op/', views.barang_op, name='barang_op'),
    path('tambah_barang/', views.tambah_barang, name='tambah_barang'),
    path('edit_barang/<int:id>', views.edit_barang, name='edit_barang'),
    path('hapus_barang/<int:id>', views.hapus_barang, name='hapus_barang'),
    path('detail_barang/<int:id>', views.detail_barang, name='detail_barang'),

    path('jenis_op/', views.jenis_op, name='jenis_op'),
    path('tambah_jenis/', views.tambah_jenis, name='tambah_jenis'),
    path('edit_jenis/<int:id>', views.edit_jenis, name='edit_jenis'),
    path('hapus_jenis/<int:id>', views.hapus_jenis, name='hapus_jenis'),

    path('peminjaman/', views.peminjaman, name='peminjaman'),
    path('hapus_pinjam/<int:id>', views.hapus_pinjam, name='hapus_pinjam'),
    path('pinjam_barang/<int:id>', views.pinjam_barang, name='pinjam_barang'),
    path('list_peminjaman/', views.list_peminjaman, name='list_peminjaman'),

    path('pengembalian/', views.pengembalian, name='pengembalian'),
    path('kembali_barang/<int:id>', views.kembali_barang, name='kembali_barang'),
    path('list_pengembalian/', views.list_pengembalian, name='list_pengembalian'),
    path('filter_pinjam/', views.filter_pinjam, name='filter_pinjam'),
    path('filter_kembali/', views.filter_kembali, name='filter_kembali'),

    path('c_pegawai', views.c_pegawai, name='c_pegawai'),
    path('c_barang', views.c_barang, name='c_barang'),
    path('c_peminjaman', views.c_peminjaman, name='c_peminjaman'),
    path('c_pengembalian', views.c_pengembalian, name='c_pengembalian'),
    path('c_f_peminjaman', views.c_f_peminjaman, name='c_f_peminjaman'),
    path('c_f_pengembalian', views.c_f_pengembalian, name='c_f_pengembalian'),
    path('coba', views.coba, name='coba'),

    path('hapus_keranjang/<int:id>', views.hapus_keranjang, name='hapus_keranjang'),
    path('hapus_keranjang2/<int:id>',
         views.hapus_keranjang2, name='hapus_keranjang2'),
    path('buat_pinjam', views.buat_pinjam, name='buat_pinjam'),
    path('pengembalian2/', views.pengembalian2, name='pengembalian2'),
    path('kembalikan', views.kembalikan, name='kembalikan'),

    path('simple_upload/', views.simple_upload, name='simple_upload'),
    path('upload_barang/', views.upload_barang, name='upload_barang'),


]
