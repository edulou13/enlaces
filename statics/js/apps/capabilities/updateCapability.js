/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .capability-sub').addClass('active');
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/prestaciones/gestion';
		}
	});
	var cap_name = $('#inputNombre').val(), btn_submit = $('button[type=submit]'), btn_del = $('#del');
	btn_del.on({
		click:function(e){
			e.preventDefault();
			btn_submit.disable().hide();
			btn_del.disable().hide();
			$.post(
				'/prestaciones/eliminar_prestacion',
				data = {'_xsrf':getCookie('_xsrf'),'id_pst':$('input[name=id_pst]').val()},
				function(response){
					if(!response){
						location.href='/prestaciones/gestion';
					} else{
						btn_submit.enable().show();
						btn_del.enable().show();
					}
				}
			);
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this);
			btn_submit.disable().hide();
			btn_del.disable().hide();
			$.post(
				'/prestaciones/modificar_prestacion',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/prestaciones/gestion';
					} else{
						//alert(oform.nombre+', está registrado.\nUse otro nombre.');
						swal({
							title: "Error!",
							text: data.nombre+', está registrado. Use otro nombre.',
							type: "error",
							confirmButtonText: "Continuar"
						});
						btn_submit.enable().show();
						btn_del.enable().show();
						$('#inputNombre').val(cap_name).focus();
					}
				}
			);
		}
	});
});