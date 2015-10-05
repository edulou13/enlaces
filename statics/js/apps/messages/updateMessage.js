/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.message-menu, .sms-catalog').addClass('active');
	$('#back, .back').on({
		click:function(e){
			e.preventDefault();
			location.href='/mensajes/gestion';
		}
	});
	$('#tipo').closest('.form-group').disable();
	$('input[name=nro_control]').disable().removeAttr('name');
	$('input[name=titulo]').addClass('only_g_names');
	var btn_submit = $('buttom[type=submit]');
	/*
	var o_key = $('.del').data('key'), btn_submit = $('buttom[type=submit]'), btn_del = $('.del');
	btn_del.removeAttr('data-key').on({
		click:function(e){
			e.preventDefault();
			btn_submit.disable().hide();
			btn_del.disable().hide();
			$.post(
				'/mensajes/eliminar_msj',
				data = {'_xsrf':getCookie('_xsrf'),'id_msj':o_key},
				function(response){
					if(response==false){
						location.href='/mensajes/gestion';
					} else{
						btn_submit.enable().show();
						btn_del.enable().show();
					}
				}
			);
		}
	});*/
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this);
			btn_submit.disable().hide();
			$.post(
				'/mensajes/modificar_msj',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/mensajes/gestion';
					} else{
						$('.check').removeClass('has-success').addClass('has-error').find('span').removeClass('fa-check').addClass('fa-times').end();
						swal({
							title:"Error!",
							text:"El Título que eligió, le pertenece a otro mensaje!",
							type:"error",
							confirmButtonText: "Continuar",//Ok
							allowEscapeKey: false
						});
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});