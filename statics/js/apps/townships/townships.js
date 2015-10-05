/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	var o_key = $('#breadcrumbs').data('key');
	$('.edit').on({
		click:function(e){
			e.preventDefault();
			location.href='/redes_salud/modificar_red?id_red='+o_key.id_red;
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
					'/redes_salud/eliminar_red',
					data = {'_xsrf': getCookie('_xsrf'), 'id_red': o_key.id_red},
					function(response){
						if(response==false){
							$('.status').text('Inhabilitado');
							o_del.remove();
							$('.add').remove();
							swal({
								title: "Inhabilitado",
								text: "La red de salud \""+o_key.str+"\", fué inhabilitada.",
								type: "success",
								confirmButtonText: "Continuar"
							});
						}
					}
				);
			});
		}
	});
	$('.add').on({
		click:function(e){
			e.preventDefault();
			location.href='/municipios/nuevo_municipio?id_red='+o_key.id_red;
		}
	});
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/redes_salud/gestion';
		}
	});
	$('#custom').customPaginator();
});