from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from xlwt.Formatting import Font
from .models import *
from inven.models import *
from .forms import *
from django.http import JsonResponse, response
import json
from django.contrib import messages
import xlwt


def dashboard_admin(request):
    if request.user.is_superuser == 1:
        user = request.user.id
        sekarang = datetime.now().date()
        list_peminjaman = peminjaman_barang.objects.all().filter(
            tanggal_pinjam=sekarang)
        total_barang = barang.objects.count()
        total_pegawai = pegawai.objects.count()
        total_peminjaman = peminjaman_barang.objects.all().count()
        total_pengembalian = pengembalian_barang.objects.all().count()

        context = {
            'semua_pinjam': list_peminjaman,
            'total_barang': total_barang,
            'total_pegawai': total_pegawai,
            'total_peminjaman': total_peminjaman,
            'total_pengembalian': total_pengembalian
        }
        return render(request, 'dashboard_admin.html', context)
    elif request.user.is_staff == 0:
        return render(request, 'eror_404.html')

# ini adalah controller (kalau di php) kalau di python kita menyebutnya views untuk barang ada tiga buah function


@login_required
def barang_admin(request):
    list_barang = barang.objects.all()
    list_pinjam = peminjaman_barang.objects.all()
    context = {
        'semua_barang': list_barang,
        'semua_pinjam': list_pinjam
    }

    if request.user.is_authenticated:
        return render(request, 'admin/barang/barang.html', context)
    else:
        return redirect('index')


@login_required
def d_barang(request, id):
    Barang = barang.objects.get(id=id)
    print(Barang.kode)
    try:
        Peminjaman = peminjaman_barang.objects.filter(
            status_peminjaman='Dipinjam').get(id_barang=Barang.kode)
        context = {
            'Barang': Barang,
            'Peminjaman': Peminjaman
        }
        return render(request, 'admin/barang/d_barang.html', context)
    except peminjaman_barang.DoesNotExist:
        return redirect('barang_admin')
# ini adalah controler atau views untuk pegawai


@login_required
def pegawai_admin(request):
    list_pegawai = pegawai.objects.all()
    context = {
        'semua_pegawai': list_pegawai
    }
    return render(request, 'admin/pegawai/pegawai.html', context)


@login_required
def d_pegawai(request, id):
    Pegawai = pegawai.objects.get(id=id)
    context = {
        'Pegawai': Pegawai,
    }
    return render(request, 'admin/pegawai/d_pegawai.html', context)

# ini adalah controller untuk laporan peminjaman barang


@login_required
def lap_peminjaman(request):
    list_peminjaman = peminjaman_barang.objects.all().select_related('barang').select_related(
        'pegawai').select_related('user').order_by('-id')
    context = {
        'semua_pinjam': list_peminjaman
    }
    if request.user.is_authenticated:
        return render(request, 'admin/laporan/lap_peminjaman.html', context)
    else:
        return redirect('index')


@login_required
def filterpinjam(request):
    dari = request.GET.get('tanggal1')
    sampai = request.GET.get('tanggal2')
    if dari == "" and sampai == "":
        return redirect('lap_peminjaman')
    elif dari == "":
        return redirect('lap_peminjaman')
    elif sampai == "":
        return redirect('lap_peminjaman')
    else:
        if request.method == 'GET':
            hasil = peminjaman_barang.objects.all().filter(
                tanggal_pinjam__range=[dari, sampai])
            context = {
                'hasil': hasil,
                'dari': dari,
                'sampai': sampai,
            }
            return render(request, 'admin/laporan/filterpinjam.html', context)

# ini adalah controller atau views untuk laporan pengembalian barang


@login_required
def lap_pengembalian(request):
    semua_kembali = peminjaman_barang.objects.all().filter(
            status_peminjaman='Dikembalikan').order_by('-id')
    context = {
        'semua_kembali': semua_kembali,
    }
    if request.user.is_superuser == 1:
        return render(request, 'admin/laporan/lap_pengembalian.html', context)
    else:
        return redirect('index')


@login_required
def filterkembali(request):
    dari = request.GET.get('tanggal1')
    sampai = request.GET.get('tanggal2')
    if dari == "" and sampai == "":
        return redirect('lap_pengembalian')
    elif dari == "":
        return redirect('lap_pengembalian')
    elif sampai == "":
        return redirect('lap_pengembalian')
    else:
        if request.method == 'GET':

            hasil = pengembalian_barang.objects.all().filter(
                tanggal_kembali__range=[dari, sampai])
            context = {
                'hasil': hasil,
                'dari': dari,
                'sampai': sampai,
            }
            return render(request, 'admin/laporan/filterkembali.html', context)


# ini adalah controller atau views untuk petugas ada tiga buah function


@login_required
def petugas(request):
    list_pengguna = User.objects.all()
    user = request.user
    nomer = user.id

    context = {
        'semua_user': list_pengguna,
    }
    if request.user.is_superuser == 1:
        return render(request, 'admin/petugas/petugas.html', context)
    elif request.user.is_staff == 0:
        return render(request, 'eror_404.html')


@login_required
def hapus_petugas(request, id):
    if request.user.is_superuser == 1:
        User.objects.filter(id=id).delete()
        return redirect('petugas')
    elif request.user.is_staff == 0:
        return render(request, 'eror_404.html')


@login_required
def tambah_petugas(request):
    if request.user.is_superuser == 1:
        form = UserForm()
        if request.method == 'POST':
            form = UserForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                messages.success(request, "Petugas berhasil di tambahkan")
                return redirect('petugas')
        context = {
            'form': form,
        }
        return render(request, 'admin/petugas/tambah_petugas.html', context)
    elif request.user.is_staff == 0:
        return render(request, 'eror_404.html')


@login_required
def ubahpass(request, id):
    if request.user.is_superuser == 1:
        petugas = User.objects.get(id=id)
        data = {
            'petugas': petugas.password,
        }
        form = ubahpassform(request.POST or None,
                            initial=data, instance=petugas)
        if request.method == 'POST':
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                messages.success(request, "password berhasil di ubah")
                return redirect('petugas')

        context = {
            'form': form,
        }
        return render(request, 'admin/petugas/ubah_pass.html', context)
    elif request.user.is_staff == 0:
        return render(request, 'eror_404.html')


@login_required
def cetak_barang(request):
    semua = barang.objects.all()
    context = {
        'semua': semua
    }
    return render(request, 'admin/laporan/c_barang.html', context)


@login_required
def cetak_peminjaman(request):
    list_peminjaman = peminjaman_barang.objects.all().select_related('barang').select_related(
        'pegawai').select_related('user').order_by('-id')
    context = {
        'semua': list_peminjaman
    }
    return render(request, 'admin/laporan/c_peminjaman.html', context)


@login_required
def cetak_pengembalian(request):
    semua_kembali = peminjaman_barang.objects.all().filter(
            status_peminjaman='Dikembalikan').order_by('-id')
    context = {
        'semua': semua_kembali,
    }
    return render(request, 'admin/laporan/c_pengembalian.html', context)


@login_required
def cetak_filter_peminjaman(request):
    if request.method == 'GET':
        dari = request.GET.get('tanggal1')
        sampai = request.GET.get('tanggal2')
        semua = peminjaman_barang.objects.all().select_related('barang').select_related('pegawai').select_related('user').filter(tanggal_pinjam__range=[dari, sampai]).order_by('-id')
        context = {
            'semua': semua,
            'dari': dari,
            'sampai': sampai,
        }
        return render(request, 'admin/laporan/c_f_peminjaman.html', context)


@login_required
def cetak_filter_pengembalian(request):
    if request.method == 'GET':
        dari = request.GET.get('tanggal1')
        sampai = request.GET.get('tanggal2')
        semua_kembali = peminjaman_barang.objects.filter(status_peminjaman='Dikembalikan').filter(tanggal_pinjam__range=[dari, sampai]).order_by('-id')
        context = {
            'semua': semua_kembali,
            'dari': dari,
            'sampai': sampai,
        }
        return render(request, 'admin/laporan/c_f_pengembalian.html', context)


@login_required
def cetak_barang_ex(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=data_barang' + \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('barang')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['nomor', 'kode barang', 'nama', 'merk', 'satuan', 'keterangan']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = barang.objects.values_list(
        'id', 'kode', 'nama', 'merk', 'satuan', 'keterangan')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


@login_required
def cetak_pegawai_ex(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=data_pegawai' + \
        str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('pegawai')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['No', 'Nama', 'Nip', 'Pangkat/golongan',
               'Jabatan']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = pegawai.objects.values_list(
        'id', 'nama', 'nip', 'pangkat_atau_golongan', 'jabatan')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response
