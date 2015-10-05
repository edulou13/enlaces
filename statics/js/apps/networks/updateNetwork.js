/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	$('.networks').on({
		click:function(e){
			e.preventDefault();
			location.href='/redes_salud/gestion';
		}
	});
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/municipios/gestion?id_red='+$('input[name=id_red]').val();
			//location.href='/redes_salud/gestion';
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			var o_form = $(this), btn_submit = $('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/redes_salud/modificar_red',
				data = o_form.form2Dict(),
				function(response){
					if(response){
						location.href='/municipios/gestion?id_red='+$('input[name=id_red]').val();
					} else{
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});