from django.contrib.auth.models import Permission, User
from django.db import models
from django.db.models import Model
from datetime import datetime, date


class barang(models.Model):
    nama = models.CharField(max_length=250)
    merk = models.CharField(max_length=100, null=True, blank=True)
    kode = models.CharField(max_length=20, null=True)
    keterangan = models.CharField(
        max_length=250, null=True, blank=True, default='-')
    Foto = models.FileField(null=True, blank=True, default='barang.jpg')
    status = models.CharField(max_length=100, default='Tersedia')

    def __str__(self):
        return self.nama


class pegawai(models.Model):
    nama = models.CharField(max_length=250)
    nip = models.CharField(max_length=250, unique=True)
    pangkat_atau_golongan = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=250)
    Foto = models.FileField(null=True, blank=True, default='karyawan.jpg')
    tanggal_terdaftar = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nama


class peminjaman_barang(models.Model):
    barang = models.ForeignKey(barang, models.CASCADE, null=True)
    pegawai = models.ForeignKey(pegawai, models.CASCADE, null=True)
    user = models.ForeignKey(User, models.CASCADE, null=True)
    kode_pinjam = models.CharField(max_length=100, null=True)
    status_peminjaman = models.CharField(
        max_length=100, default='Dipinjam')
    tanggal_pinjam = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nama_peminjam


class pengembalian_barang(models.Model):
    peminjaman_barang = models.ForeignKey(
        peminjaman_barang, models.CASCADE, null=True)
    tanggal_kembali = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nama_pengembali


class keranjang(models.Model):
    barang = models.ForeignKey(barang, models.CASCADE, null=True)
    user = models.ForeignKey(User, models.CASCADE, null=True)

    def __str__(self):
        return self.nama_barang
