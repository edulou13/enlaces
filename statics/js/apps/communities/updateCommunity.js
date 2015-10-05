/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	var o_key = $('.breadcrumb').data('key');
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
	$('.mup').on({
		click:function(e){
			e.preventDefault();
			location.href='/comunidades/gestion?id_mup='+o_key.mup;
		}
	});
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='centros_salud/gestion?id_com='+$('input[name=id_com]').val();
		}
	});
	$('form').on({
		submit:function(e){
			var o_form = $(this), btn_submit = $('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/comunidades/modificar_comunidad',
				data = o_form.form2Dict(),
				function(response){
					if(response){
						location.href='centros_salud/gestion?id_com='+$('input[name=id_com]').val();
					} else{
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});