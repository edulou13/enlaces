/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	$.each($('#custom .del'), function(){
		$(this).on({
			click:function(e){
				e.preventDefault();
				var o_cen = $(this).data('key'), o_del = $(this);
				swal({
					title: "Está seguro?",
					text: o_cen.nombre+", será inhabilitado!",
					type: "warning",
					showCancelButton: true,
					cancelButtonText: "Cancelar",
					confirmButtonClass: "btn-danger",
					confirmButtonText: "Inhabilitar",
					closeOnConfirm: false
				}, function(){
					$.post(
						'/centros_salud/eliminar_establecimiento',
						data = {'_xsrf':getCookie('_xsrf'),'id_cen':o_cen.id},
						function(response){
							if(response==false){
								o_del.closest('tr').find('.activo').html('Inhabilitado').end().find('.comunidades').html('0').end().find('.prestaciones').html('0').end().end().remove();
								swal({
									title: "Inhabilitado",
									text: "El establecimiento de salud \""+o_cen.nombre+"\", fué inhabilitado.",
									type: "success",
									confirmButtonText: "Continuar"
								});
							}
						}
					);
				});
			}
		});
	});
	var o_key = $('.breadcrumb').data('key');
	$('#add').on({
		click:function(e){
			e.preventDefault();
			location.href='/centros_salud/nuevo_establecimiento?id_com='+o_key.com;
		}
	});
	$('.delete').on({
		click:function(e){
			e.preventDefault();
			swal({
				title: 'Está seguro?',
				text: o_key.str+', será inhabilitado!',
				type: "warning",
				showCancelButton: true,
				cancelButtonText: "Cancelar",
				confirmButtonClass: "btn-danger",
				confirmButtonText: "Inhabilitar",
				closeOnConfirm: false
			}, function(){
				$.post(
					'/comunidades/elimininar_comunidad',
					data = {'_xsrf':getCookie('_xsrf'), 'id_com':o_key.com},
					function(response){
						if(!response){
							$('.status').text('Inhabilitado');
							$('#add, .delete').remove();
							swal({
								title: 'Inhabilitado',
								text: 'La comunidad "'+o_key.str+'", fué inhabilitado.',
								type: 'success',
								confirmButtonText: 'Continuar'
							});
						}
					}
				);
			});
		}
	});
	$('.networks').on({
		click:function(e){
			e.preventDefault();
			location.href='/redes_salud/gestion';
		}
	});
	$('.net').on({
		click:function(e){
			e.preventDefault();
			location.href='/municipios/gestion?id_red='+o_key.red;
		}
	});
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/comunidades/gestion?id_mup='+o_key.mup;
		}
	});
	$('.edit').on({
		click:function(e){
			e.preventDefault();
			location.href='/comunidades/modificar_comunidad?id_com='+o_key.com;
		}
	});
	$('#custom').customPaginator();
});