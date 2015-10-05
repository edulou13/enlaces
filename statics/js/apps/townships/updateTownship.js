/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	var dptos = ['BENI', 'COCHABAMBA', 'CHUQUISACA', 'LA PAZ', 'ORURO', 'PANDO', 'POTOSÍ', 'SANTA CRÚZ', 'TARIJA'],
		options = [], o_key = $('.breadcrumb').data('key');
	// console.log(o_key);
	for (var i = 0; i < dptos.length; i++) {
		if(o_key.dpto==dptos[i]){
			options.push('<option value="'+dptos[i]+'" selected>'+dptos[i]+'</option>');
		} else{
			options.push('<option value="'+dptos[i]+'">'+dptos[i]+'</option>');
		}
	};
	$('#inputDpto').html(options.join(''));
	$('.networks').on({
		click:function(e){
			e.preventDefault();
			location.href='/redes_salud/gestion';
		}
	});
	$('.net').on({
		click:function(e){
			e.preventDefault();
			location.href='/municipios/gestion?id_red='+o_key.id_red;
		}
	});
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/comunidades/gestion?id_mup='+$('input[name=id_mup]').val();
			//location.href='/municipios/gestion?id_red='+o_key.id;
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			var o_form = $(this), btn_submit = $('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/municipios/modificar_municipio',
				data = o_form.form2Dict(),
				function(response){
					if(response){
						location.href='/comunidades/gestion?id_mup='+$('input[name=id_mup]').val();
					} else{
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});