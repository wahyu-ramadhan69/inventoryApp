from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.html import format_html
from .models import *
from .forms import *
from .resources import *
from tablib import Dataset
from django.http import JsonResponse
import json
from django.db.models import Max


from django.contrib import messages

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


# ini adalah controller atau view untuk halaman operator view ini hanya bisa di akses oleh user biasa

@login_required
def dashboard_op(request):
    nomer = request.user.id
    if request.user.is_superuser == 0:
        sekarang = datetime.now().date()
        semua_pinjam = peminjaman_barang.objects.all().select_related('barang').select_related('pegawai').select_related('user').filter(tanggal_pinjam=sekarang).filter(user=nomer).order_by('-id')
        list_peminjaman = peminjaman_barang.objects.all().filter(
            tanggal_pinjam=sekarang).filter(user=nomer)
        total_barang = barang.objects.count()
        total_pegawai = pegawai.objects.count()
        total_peminjaman = peminjaman_barang.objects.all().filter(user=nomer).count()

        context = {
            'semua_pinjam': semua_pinjam,
            'total_barang': total_barang,
            'total_pegawai': total_pegawai,
            'total_peminjaman': total_peminjaman
        }
        return render(request, 'dashboard_operator.html', context)
    elif request.user.is_staff == 1:
        return render(request, 'eror_404.html')

# ini adalah controller atau view manajemen data pegawai


@login_required
def pegawai_op(request):
    list_pegawai = pegawai.objects.all()
    form = PegawaiForm()
    if request.method == 'POST':
        form = PegawaiForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Data pegawai berhasil di tambahkan")
            return redirect('pegawai_op')
        else:
            messages.error(request, "Nip sudah pernah di daftarkan")
            return redirect('pegawai_op')
    context = {
        'semua_pegawai': list_pegawai
    }
    if request.user.is_superuser == 0:
        return render(request, 'operator/pegawai/pegawai.html', context)
    elif request.user.is_staff == 1:
        return render(request, 'eror_404.html')


@login_required
def simple_upload(request):
    if request.method == 'POST':
        kubsum = pegawaisumber()
        dataset = Dataset()
        data = request.FILES['myfile']

        imported_data = dataset.load(data.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:
            print(data[1])
            value = pegawai(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
            )
            value.save()

        # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return redirect('pegawai_op')


@login_required
def upload_barang(request):
    if request.method == 'POST':
        dataset = Dataset()
        data = request.FILES['myfile']

        imported_data = dataset.load(data.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:
            print(data[1])
            value = barang(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
            )
            value.save()

        # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return redirect('barang_op')


@login_required
def tambahpegawai(request):
    form = PegawaiForm()
    if request.method == 'POST':
        form = PegawaiForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Data pegawai berhasil di tambahkan")
            return redirect('pegawai_op')
        else:
            messages.error(request, "Nip sudah pernah di daftarkan")
            return redirect('pegawai_op')
    return render(request, 'operator/pegawai/tambah_pegawai.html', {
        'form': form
    })


@login_required
def edit_pegawai(request, id):
    Pegawai = pegawai.objects.get(id=id)
    data = {
        'nama': Pegawai.nama,
        'nip': Pegawai.nip,
        'pangkat_atau_golongan': Pegawai.pangkat_atau_golongan,
        'jabatan': Pegawai.jabatan,
        'Foto': Pegawai.Foto,
    }
    form = PegawaiForm(request.POST or None,
                       request.FILES or None, initial=data, instance=Pegawai)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Data pegawai berhasil di ubah")
            return redirect('pegawai_op')

    context = {
        'form': form,
        'Pegawai': Pegawai,
    }
    return render(request, 'operator/pegawai/edit_pegawai.html', context)


@login_required
def detail_pegawai(request, id):
    Pegawai = pegawai.objects.get(id=id)
    context = {
        'Pegawai': Pegawai,
    }
    return render(request, 'operator/pegawai/detail_pegawai.html', context)


@login_required
def hapus_pegawai(request, id):
    if request.user.is_superuser == 0:
        pegawai.objects.filter(id=id).delete()
        return redirect('pegawai_op')
    elif request.user.is_staff == 1:
        return render(request, 'eror_404.html')


@login_required
def barang_op(request):
    list_barang = barang.objects.all()
    if not list_barang:
        kode = 'BR001'
        context = {
            'semua_barang': list_barang,
            'kode': kode
        }
        if request.user.is_superuser == 0:
            return render(request, 'operator/barang/barang.html', context)
        elif request.user.is_staff == 1:
            return render(request, 'eror_404.html')
    else:
        max = barang.objects.latest('id').id
        maxi = max + 1
        kode = 'BR00' + str(maxi)
        context = {
            'semua_barang': list_barang,
            'kode': kode
        }
        if request.user.is_superuser == 0:
            return render(request, 'operator/barang/barang.html', context)
        elif request.user.is_staff == 1:
            return render(request, 'eror_404.html')


@login_required
def tambah_barang(request):
    if request.user.is_superuser == 0:
        list = barang.objects.all()
        if not list:
            kode = 'BR001'
            form = BarangForm()
            if request.method == 'POST':
                form = BarangForm(request.POST or None, request.FILES or None)
                if form.is_valid():
                    form.save()
                    messages.success(request, "barang berhasil di tambahkan")
                    return redirect('barang_op')
        else:
            max = barang.objects.latest('id').id
            maxi = max + 1
            kode = 'BR00' + str(maxi)
            print(kode)
            form = BarangForm()
            if request.method == 'POST':
                form = BarangForm(request.POST or None, request.FILES or None)
                if form.is_valid():
                    form.save()
                    messages.success(request, "barang berhasil di tambahkan")
                    return redirect('barang_op')
        return redirect('barang_op')
    else:
        return render(request, 'eror_404.html')


def hapus_barang(request, id):
    if request.user.is_superuser == 0:
        barang.objects.filter(id=id).delete()
        return redirect('barang_op')
    else:
        return render(request, 'eror_404.html')


def edit_barang(request, id):
    Barang = barang.objects.get(id=id)
    data = {
        'nama': Barang.nama,
        'merk': Barang.merk,
        'keterangan': Barang.keterangan,
        'Foto': Barang.Foto,
    }
    form = BarangForm(request.POST or None,
                      request.FILES or None, initial=data, instance=Barang)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Data barang berhasil di ubah")
            return redirect('barang_op')

    context = {
        'form': form,
        'Barang': Barang
    }
    print(Barang.Foto.url)
    return render(request, 'operator/barang/update_barang.html', context)



def detail_barang(request, id):
    Barang = barang.objects.get(id=id)
    context = {
        'Barang': Barang,
    }
    return render(request, 'operator/barang/detail_barang.html', context)


@login_required
def jenis_op(request):
    list_jenis = jenis.objects.all()
    context = {
        'semua_jenis': list_jenis
    }
    if request.user.is_superuser == 0:
        return render(request, 'operator/jenis/jenis.html', context)
    elif request.user.is_staff == 1:
        return render(request, 'eror_404.html')


@login_required
def tambah_jenis(request):
    if request.user.is_superuser == 0:
        form = jenisbarang()
        if request.method == 'POST':
            form = jenisbarang(request.POST or None, request.FILES or None)
            if form.is_valid():
                form.save()
                messages.success(request, "jenis barang berhasil di tambahkan")
            return redirect('jenis_op')
        else:
            return render(request, 'operator/jenis/tambah_jenis_barang.html', {
                'form': form
            })
    else:
        return render(request, 'eror_404.html')


@login_required
def edit_jenis(request, id):
    if id == 4:
        return render(request, 'eror_404.html')
    else:
        if request.user.is_superuser == 0:
            Jenis = jenis.objects.get(id=id)
            data = {
                'nama': Jenis.nama,
                'deskripsi': Jenis.deskripsi,
            }
            form = jenisbarang(request.POST or None,
                               request.FILES or None, initial=data, instance=Jenis)
            if request.method == 'POST':
                if form.is_valid():
                    form.save()
                    messages.success(
                        request, "Data Jenis barang berhasil di ubah")
                    return redirect('jenis_op')

            context = {
                'form': form,
                'Jenis': Jenis
            }
            return render(request, 'operator/jenis/ubah_jenis.html', context)
        else:
            return render(request, 'eror_404.html')


@login_required
def hapus_jenis(request, id):
    if id == 4:
        return render(request, 'eror_404.html')
    else:
        if request.user.is_superuser == 0:
            jenis.objects.filter(id=id).delete()
            return redirect('jenis_op')
        else:
            return render(request, 'eror_404.html')


@login_required
def peminjaman(request):
    User = request.user.id
    Keranjang = keranjang.objects.select_related('barang')
    if request.user.is_superuser == 0:
        if request.method == 'GET':
            keyword = request.GET.get('keyword', '')
            hasil = barang.objects.filter(
                nama__icontains=keyword).distinct().filter(status='Tersedia')
            context = {
                'hasil': hasil,
                'User': User,
                'Keranjang': Keranjang
            }
            return render(request, 'operator/transaksi/peminjaman.html', context)
        elif request.method == 'POST':
            id = request.POST.get('barang')
            form = keranjangbarang(request.POST or None)
            Barang = barang.objects.get(id=id)
            data = {
                'status': Barang.status
            }
            update_barang = statusbarang2(
                request.POST or None, initial=data, instance=Barang)
            if form.is_valid() and update_barang.is_valid():
                simpan = form.save()
                update = update_barang.save(commit=False)
                simpan.save()
                update.save()
                return redirect("peminjaman")
            else:
                return redirect('list_peminjaman')
    else:
        return render(request, 'eror_404.html')


@login_required
def hapus_keranjang(request, id):
    Keranjang = keranjang.objects.get(id=id)
    barang_id = request.POST.get("id")
    Barang = barang.objects.get(id=barang_id)
    data = {
        'status': Barang.status
    }
    update_barang = statusbarang(
        request.POST or None, initial=data, instance=Barang)
    if update_barang.is_valid():
        update = update_barang.save(commit=False)
        update.save()
        keranjang.objects.filter(id=id).delete()
        return redirect('peminjaman')


@login_required
def hapus_keranjang2(request, id):
    Keranjang = keranjang.objects.get(id=id)
    barang_id = request.POST.get("id")
    Barang = barang.objects.get(id=barang_id)
    data = {
        'status': Barang.status
    }
    update_barang = statusbarang(
        request.POST or None, initial=data, instance=Barang)
    if update_barang.is_valid():
        update = update_barang.save(commit=False)
        update.save()
        keranjang.objects.filter(id=id).delete()
        return redirect('buat_pinjam')


@login_required
def buat_pinjam(request):
    data = keranjang.objects.all()
    if not data:
        return redirect('peminjaman')
    else:
        nama_op = request.user.id
        nama = request.POST.get('nama_peminjam')
        nip = request.POST.get('nip_peminjam')
        no = request.POST.get('id_peminjam')
        pinjam = peminjaman_barang.objects.all()
        if not pinjam:
            kode = 'PJ001'
            Keranjang2 = keranjang.objects.select_related('barang')
            Keranjang = keranjang.objects.all()
            if request.method == 'POST':
                for x in Keranjang:
                    simpan = peminjaman_barang(
                        kode_pinjam=kode, barang_id=x.barang.id, pegawai_id=no, user_id=nama_op)
                    simpan.save()
                keranjang.objects.all().delete()
                return redirect('list_peminjaman')

            context = {
                'Keranjang': Keranjang,
                'Keranjang2': Keranjang2,
                'kode': kode
            }
            return render(request, 'operator/transaksi/buat_pinjam2.html', context)
        else:
            Keranjang2 = keranjang.objects.select_related('barang')
            max = peminjaman_barang.objects.latest('id').id
            maxi = max + 1
            kode = 'PJ00' + str(maxi)
            print(kode)

            Keranjang = keranjang.objects.all()
            if request.method == 'POST':
                for x in Keranjang2:
                    simpan = peminjaman_barang(
                        kode_pinjam=kode, barang_id=x.barang.id, pegawai_id=no, user_id=nama_op)
                    simpan.save()
                keranjang.objects.all().delete()
                return redirect('list_peminjaman')

            context = {
                'Keranjang': Keranjang,
                'kode': kode
            }
            return render(request, 'operator/transaksi/buat_pinjam2.html', context)


@login_required
def pinjam_barang(request, id):
    User = request.user.username
    Barang = barang.objects.get(id=id)
    Pegawai = pegawai.objects.all()
    data = {
        'id': Barang.id,
        'nama': Barang.nama,
        'jenis': Barang.jenis,
        'status': Barang.status,
        'keterangan': Barang.keterangan,
        'Foto': Barang.Foto,
    }
    form_barang = statusbarang(
        request.POST or None, initial=data, instance=Barang)
    form_pinjam = PinjamBarang(request.POST or None)
    if form_barang.is_valid() and form_pinjam.is_valid():
        instance = form_barang.save(commit=False)
        pinjam = form_pinjam.save()
        jenis = request.POST.get('jenis')
        if jenis == 'atk':
            pinjam.status_peminjaman = 'Sekali pakai'
            instance.status = 'habis'
            instance.save()
            pinjam.save()
            messages.success(request, "Peminjaman barang berhasil di lakukan")
            return redirect('list_peminjaman')

        else:
            pinjam.save()
            instance.save()
            messages.success(request, "Peminjaman berhasil di lakukan")
            return redirect('list_peminjaman')
        return redirect('peminjaman')

    context = {
        'Barang': Barang,
        'Pegawai': Pegawai,
        'form': form_pinjam,
        'User': User,
    }
    print(User)
    return render(request, 'operator/transaksi/buat_pinjam.html', context)


@login_required
def hapus_pinjam(request, id):
    Pinjam = peminjaman_barang.objects.get(id=id)
    Barang = barang.objects.get(id=Pinjam.barang_id)
    data = {
        'status': Barang.status
    }
    update_barang = statusbarang(
        request.POST or None, initial=data, instance=Barang)
    if update_barang.is_valid():
        update = update_barang.save(commit=False)
        update.status = 'Tersedia'
        update.save()
        peminjaman_barang.objects.filter(id=id).delete()
        return redirect('list_peminjaman')


@login_required
def list_peminjaman(request):
    nomer = request.user.id
    semua_pinjam = peminjaman_barang.objects.all().select_related('barang').select_related(
        'pegawai').select_related('user').filter(user=nomer).order_by('-id')
    context = {
        'semua_pinjam': semua_pinjam
    }
    return render(request, 'operator/transaksi/list_pinjam.html', context)


@login_required
def filter_pinjam(request):
    dari = request.GET.get('tanggal1')
    sampai = request.GET.get('tanggal2')
    if dari == "" and sampai == "":
        return redirect('list_peminjaman')
    else:
        if request.method == 'GET':
            nomer = request.user.id
            hasil = peminjaman_barang.objects.all().select_related('barang').select_related('pegawai').select_related('user').filter(tanggal_pinjam__range=[dari, sampai]).filter(user=nomer).order_by('-id')
            context = {
                'hasil': hasil,
                'dari': dari,
                'sampai': sampai,
            }
            return render(request, 'operator/transaksi/filterpinjam.html', context)


@login_required
def pengembalian2(request):
    nama = request.GET.get('nama')
    nip = request.GET.get('nip')
    id = request.GET.get('id')
    peminjam = request.POST.get('nama_pengembali')
    nip_peminjam = request.POST.get('nip_pengembali')
    User = request.user.username
    nomer = request.POST.get('id_transaksi')
    if request.method == 'GET':
        nama = request.GET.get('nama')
        nip = request.GET.get('nip')
        keyword = request.GET.get('keyword', '')
        hasil = peminjaman_barang.objects.filter(
            kode_pinjam__icontains=keyword).distinct().select_related('barang').filter(status_peminjaman='Dipinjam')
        context = {
            'User': User,
            'hasil': hasil,
            'nama': nama,
            'nip': nip
        }
        return render(request, 'operator/transaksi/buat_kembali.html', context)
    elif request.method == 'POST':
        Peminjaman = peminjaman_barang.objects.get(id=nomer)
        Barang = barang.objects.get(kode=Peminjaman.id_barang)
        data = {
            'status': Barang.status
        }
        update_barang = statusbarang(
            request.POST or None, initial=data, instance=Barang)
        update_pinjam = statuspinjam(
            request.POST or None, instance=Peminjaman)
        pengembalian = KembaliBarang(
            request.POST or None, request.FILES or None)

        if update_barang.is_valid() and update_pinjam.is_valid() and pengembalian.is_valid():
            update1 = update_barang.save(commit=False)
            update2 = update_pinjam.save(commit=False)
            kembali = pengembalian.save()
            update1.save()
            update2.save()
            kembali.save()

            hasil = peminjaman_barang.objects.filter(
                kode_pinjam__icontains=peminjam).distinct().filter(status_peminjaman='Dipinjam')
            context = {
                'User': User,
                'hasil': hasil,
                'peminjam': peminjam,
                'nip_peminjam': nip_peminjam
            }
            return render(request, 'operator/transaksi/buat_kembali2.html', context)


@login_required
def kembali_barang(request, id):
    Peminjaman = peminjaman_barang.objects.get(id=id)
    Barang = barang.objects.get(id=Peminjaman.barang_id)
    data = {
        'status': Barang.status
    }
    update_barang = statusbarang(
        request.POST or None, initial=data, instance=Barang)
    update_pinjam = statuspinjam(request.POST or None, instance=Peminjaman)

    kembali = KembaliBarang(request.POST or None)
    if request.method == 'POST':
        if update_barang.is_valid() and update_pinjam.is_valid() and kembali.is_valid():
            update = update_barang.save(commit=False)
            update2 = update_pinjam.save(commit=False)
            update2.save()
            update.save()
            kembali.save()
            return redirect('pengembalian')


def kembalikan(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        hasil = peminjaman_barang.objects.all()
        context = {
            'hasil': hasil

        }
        return render(request, 'operator/transaksi/buat_kembali.html', context)


@login_required
def pengembalian(request):
    User = request.user.username
    if request.user.is_superuser == 0:
        if request.method == 'GET':
            keyword = request.GET.get('keyword', '')
            hasil = peminjaman_barang.objects.all().select_related('barang').select_related(
                'pegawai').select_related('user').filter(
                kode_pinjam__icontains=keyword).distinct().filter(status_peminjaman='Dipinjam')
            context = {
                'User': User,
                'hasil': hasil
            }
            return render(request, 'operator/transaksi/pengembalian.html', context)
        elif request.method == 'POST':
            keyword = request.POST.get('keyword', '')
            hasil = peminjaman_barang.objects.filter(
                kode_pinjam__icontains=keyword).distinct().filter(status_peminjaman='Dipinjam')
            context = {
                'User': User,
                'hasil': hasil
            }
            return render(request, 'operator/transaksi/buat_kembali.html', context)
    else:
        return render(request, 'eror_404.html')


@login_required
def list_pengembalian(request):
    if request.user.is_superuser == 0:
        user = request.user.username
        semua_kembali = peminjaman_barang.objects.all().filter(
            status_peminjaman='Dikembalikan').order_by('-id')
        semua = peminjaman_barang.objects.filter(
            pengembalian_barang__isnull=True).values_list('kode_pinjam', flat=True)
        context = {
            'semua_kembali': semua_kembali,
            'semua': semua
        }
        return render(request, 'operator/transaksi/list_kembali.html', context)
    else:
        return render(request, 'eror_404.html')


@login_required
def filter_kembali(request):
    dari = request.GET.get('tanggal1')
    sampai = request.GET.get('tanggal2')
    if dari == "" and sampai == "":
        return redirect('list_peminjaman')
    else:
        if request.method == 'GET':
            user = request.user.username
            hasil = pengembalian_barang.objects.all().filter(
                tanggal_kembali__range=[dari, sampai]).filter(nama_op=user)
            context = {
                'hasil': hasil,
                'dari': dari,
                'sampai': sampai,
            }
            return render(request, 'operator/transaksi/filterkembali.html', context)


@login_required
def c_pegawai(request):
    semua = pegawai.objects.all()
    context = {
        'semua': semua
    }
    return render(request, 'operator/laporan/c_pegawai.html', context)


@login_required
def c_barang(request):
    semua = barang.objects.all()
    context = {
        'semua': semua
    }
    return render(request, 'operator/laporan/c_barang.html', context)


@login_required
def c_peminjaman(request):
    user = request.user.id
    # semua = peminjaman_barang.objects.raw(
    # 'SELECT * FROM inven_peminjaman_barang JOIN inven_barang ON inven_peminjaman_barang.barang_id = inven_barang.id JOIN inven_pegawai ON inven_peminjaman_barang.`pegawai_id` = inven_pegawai.`id` WHERE inven_peminjaman_barang.`user_id` = 2')
    semua = peminjaman_barang.objects.all().select_related('barang').select_related('pegawai').filter(user_id=user).order_by('-id')
    context = {
        'semua': semua
    }
    return render(request, 'operator/laporan/c_peminjaman.html', context)


@login_required
def c_pengembalian(request):
    semua_kembali = peminjaman_barang.objects.all().filter(status_peminjaman='Dikembalikan').order_by('-id')
    semua = peminjaman_barang.objects.filter(pengembalian_barang__isnull=True).values_list('kode_pinjam', flat=True)
    context = {
        'semua_kembali': semua_kembali,
        'semua': semua
    }
    return render(request, 'operator/laporan/c_pengembalian.html', context)


@login_required
def c_f_peminjaman(request):
    if request.method == 'GET':
        user = request.user.username
        dari = request.GET.get('tanggal1')
        sampai = request.GET.get('tanggal2')
        if dari == "":
            return redirect('peminjaman')
        else:
            semua = peminjaman_barang.objects.all().filter(
                tanggal_pinjam__range=[dari, sampai]).filter(nama_op=user)
            context = {
                'semua': semua,
                'dari': dari,
                'sampai': sampai,
            }
            return render(request, 'operator/laporan/c_f_peminjaman.html', context)


@login_required
def c_f_pengembalian(request):
    if request.method == 'GET':
        user = request.user.id
        dari = request.GET.get('tanggal1')
        sampai = request.GET.get('tanggal2')
        semua = pengembalian_barang.objects.all().filter(
            tanggal_kembali__range=[dari, sampai])
        context = {
            'semua': semua,
            'dari': dari,
            'sampai': sampai,
        }
        return render(request, 'operator/laporan/c_f_pengembalian.html', context)


def coba(request):
    kode = barang.objects.aggregate(Max('kode'))
    kode2 = barang.objects.all().aggregate(Max('kode'))
    print(kode)
    print(kode2)

    context = {
        'kode': kode
    }

    return render(request, 'test.html', context)
