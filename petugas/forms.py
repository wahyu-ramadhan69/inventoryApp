from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from inven.models import *


class BarangForm(forms.ModelForm):
    class Meta:
        model = barang
        fields = ['nama', 'merk', 'kode', 'keterangan', 'Foto']

    def __init__(self, *args, **kwargs):
        super(BarangForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'field tidak boleh kosong'.format(
                nama=field.label)}


class keranjangbarang(forms.ModelForm):
    class Meta:
        model = keranjang
        fields = ['barang', 'user']


class PegawaiForm(forms.ModelForm):
    class Meta:
        model = pegawai
        fields = ['nama', 'nip', 'pangkat_atau_golongan', 'jabatan', 'Foto']

    def __init__(self, *args, **kwargs):
        super(PegawaiForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'field tidak boleh kosong'.format(
                nama=field.label)}


class statusbarang(forms.ModelForm):
    class Meta:
        model = barang
        fields = ['status', 'keterangan']


class statusbarang2(forms.ModelForm):
    class Meta:
        model = barang
        fields = ['status']


class statuspinjam(forms.ModelForm):
    class Meta:
        model = peminjaman_barang
        fields = ['status_peminjaman']


class KembaliBarang(forms.ModelForm):
    class Meta:
        model = pengembalian_barang
        fields = ['peminjaman_barang']

    def __init__(self, *args, **kwargs):
        super(KembaliBarang, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': 'field tidak boleh kosong'.format(
                nip_pengembali=field.label)}


class PinjamBarang(forms.ModelForm):
    class Meta:
        model = peminjaman_barang
        fields = ['barang', 'pegawai',
                  'user', 'kode_pinjam']
