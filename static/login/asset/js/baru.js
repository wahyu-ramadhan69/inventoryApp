const flashdata = $('.flash-datas').data('flashdata');

if (flashdata) {
	Swal.fire({
		position: 'center',
		type: 'warning',
		title: flashdata,
		showConfirmButton: false,
		timer: 2000
	})
}
