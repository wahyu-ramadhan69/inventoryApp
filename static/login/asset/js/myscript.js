const flashdata = $('.flash-data').data('flashdata');

if (flashdata) {
	Swal.fire({
		position: 'center',
		type: 'success',
		title: 'Data Berhasil ' + flashdata,
		showConfirmButton: false,
		timer: 2000
	})
}


//tombol-hapus
$('.tombol-hapus').on('click', function (e) {

	e.preventDefault();

	const swalWithBootstrapButtons = Swal.mixin({
		confirmButtonClass: 'btn btn-success',
		cancelButtonClass: 'btn btn-danger',
		buttonsStyling: false,
	})

	const href = $(this).attr('href');
	swalWithBootstrapButtons.fire({
		title: 'Apakah anda yakin ?',
		text: "Data akan dihapus",
		type: 'warning',
		showCancelButton: true,
		confirmButtonText: 'Hapus Data',
		cancelButtonText: 'Batal',
		reverseButtons: true
	}).then((result) => {
		if (result.value) {
			document.location.href = href;
		} else if (
			// Read more about handling dismissals
			result.dismiss === Swal.DismissReason.cancel
		) {
			swalWithBootstrapButtons.fire(
				'Dibatalkan',
				'Data masih aman :)',
				'error'
			)
		}
	})

});

//tombol-acc
$('.tombol-acc').on('click', function (e) {

	e.preventDefault();

	const swalWithBootstrapButtons = Swal.mixin({
		confirmButtonClass: 'btn btn-success',
		cancelButtonClass: 'btn btn-danger',
		buttonsStyling: false,
	})

	const href = $(this).attr('href');
	swalWithBootstrapButtons.fire({
		title: 'Apakah anda yakin ?',
		text: "Data Laporan akhir akan di acc",
		type: 'warning',
		showCancelButton: true,
		confirmButtonText: 'Acc',
		cancelButtonText: 'Batal',
		reverseButtons: true
	}).then((result) => {
		if (result.value) {
			document.location.href = href;
		} else if (
			// Read more about handling dismissals
			result.dismiss === Swal.DismissReason.cancel
		) {
			swalWithBootstrapButtons.fire(
				'Dibatalkan',
				'Data laporan akhir skripsi belum di acc :)',
				'error'
			)
		}
	})

});
