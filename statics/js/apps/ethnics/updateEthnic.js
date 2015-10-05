/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .ethnic-sub').addClass('active');
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/etnias/gestion';
		}
	});
	var eth_name = $('#inputNombre').val(), btn_submit = $('button[type=submit]'), btn_del = $('#del');
	btn_del.on({
		click:function(e){
			e.preventDefault();
			btn_submit.disable().hide();
			btn_del.disable().hide();
			$.post(
				'/etnias/eliminar_etnia',
				data = {'_xsrf':getCookie('_xsrf'),'id_etn':$('input[name=id_etn]').val()},
				function(response){
					if(response==false){
						location.href='/etnias/gestion';
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
			var oform = $(this), btn_submit = oform.find('button[type=submit]');
			//console.log(oform);
			btn_submit.disable().hide();
			$.post(
				'/etnias/modificar_etnia',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/etnias/gestion';
					} else{
						//alert(oform.nombre+', ya está registrado.\nEscoja otro nombre.');
						swal({
							title: "Error!",
							text: data.nombre+', está registrado. Use otro nombre.',
							type: "error",
							confirmButtonText: "Continuar"
						});
						btn_submit.enable().show()
						$('#inputNombre').val(eth_name).focus();
					}
				}
			);
		}
	});
});