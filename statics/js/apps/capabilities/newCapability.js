/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .capability-sub').addClass('active');
	$('button[type=button], .back').on({
		click:function(e){
			e.preventDefault();
			location.href='/prestaciones/gestion';
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this), btn_submit = oform.find('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/prestaciones/nueva_prestacion',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/prestaciones/gestion';
					} else{
						//alert(form.nombre+', está registrado.\nUse otro nombre.');
						swal({
							title: "Error!",
							text: data.nombre+", está registrado. Use otro nombre.",
							type: "error",
							confirmButtonText: "Continuar"
						});
						btn_submit.enable().show();
						$('#inputNombre').val('').focus();
					}
				}
			);
		}
	});
});