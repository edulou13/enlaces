/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .ethnic-sub').addClass('active');
	$('button[type=button], .back').on({
		click:function(e){
			e.preventDefault();
			location.href='/etnias/gestion';
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this), btn_submit = $(this).find('button[type=submit]');
			//console.log(oform.form2Dict());
			btn_submit.disable().hide();
			$.post(
				'/etnias/nueva_etnia',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/etnias/gestion';
					} else{
						//alert(data.nombre+', ya está registrado.\nEscoja otro nombre.');
						swal({
							title: "Error!",
							text: data.nombre+', está registrado. Use otro nombre.',
							type: "error",
							confirmButtonText: "Continuar"
						});
						$('input[name=nombre]').val('').focus();
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});