/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	var o_key = $('.breadcrumb').data('key');
	$('.edit').on({
		click:function(e){
			e.preventDefault();
			location.href='/municipios/modificar_municipio?id_mup='+o_key.mup;
		}
	});
	$('.delete').on({
		click:function(e){
			e.preventDefault();
			var o_del = $(this);
			swal({
				title: "Está seguro?",
				text: o_key.str+", será inhabilitado!",
				type: "warning",
				showCancelButton: true,
				cancelButtonText: "Cancelar",
				confirmButtonClass: "btn-danger",
				confirmButtonText: "Inhabilitar",
				closeOnConfirm: false
			}, function(){
				$.post(
					'/municipios/eliminar_municipio',
					data = {'_xsrf':getCookie('_xsrf'),'id_mup':o_key.mup},
					function(response){
						if(response==false){
							$('.status').text('Inhabilitado');
							$('.add').remove();
							o_del.remove();
							swal({
								title: "Eliminado",
								text: "El municipio \""+o_key.str+"\", fué inhabilitado.",
								type: "success",
								confirmButtonText: "Continuar"
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
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/municipios/gestion?id_red='+o_key.red;
		}
	});
	$('.add').on({
		click:function(e){
			e.preventDefault();
			location.href='/comunidades/nueva_comunidad?id_mup='+o_key.mup;
		}
	});
	$('#custom').customPaginator();
});