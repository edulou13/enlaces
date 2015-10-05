/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .type-sub').addClass('active');
	$('button[type=button], .back').on({
		click:function(e){
			e.preventDefault();
			location.href='/tipos/gestion';
		}
	});
	var tip_name = $('#inputNombre').val();
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this), btn_submit = oform.find('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/tipos/modificar_tipo',
				data = oform.form2Dict(),
				function(response){
					//console.log('status: ',response);
					if(response){
						location.href='/tipos/gestion';
					} else{
						swal({
							title: "Error!",
							text: data.nombre+", está registrado. Use otro nombre.",
							type: "error",
							confirmButtonText: "Continuar"
						});
						btn_submit.enable().show()
						$('#inputNombre').val(tip_name).focus();
					}
				}
			);
		}
	});
});