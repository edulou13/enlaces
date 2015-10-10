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
		}
	});
	var dptos = ['BENI', 'COCHABAMBA', 'CHUQUISACA', 'LA PAZ', 'ORURO', 'PANDO', 'POTOSÍ', 'SANTA CRÚZ', 'TARIJA'],
		options = [], count = 0
		tmpl = function(n){
			return '<div class="row comunidad-'+n+'">'+
			'<div class="form-group has-feedback col-sm-7">'+
				'<label for="inputNombre">Nombre:</label>'+
				'<input type="text" name="nombre" id="inputNombre" class="form-control input-sm only_g_names" required>'+
				'<span class="form-control-feedback"></span>'+
			'</div>'+
			'<div class="form-group has-feedback col-sm-5">'+
				'<label for="inputTelf">Celular:</label>'+
				'<input type="text" name="telf" id="inputTelf" class="form-control input-sm only_cell_phone">'+
				'<span class="form-control-feedback"></span>'+
			'</div></div>';
		};
	for (var i = 0; i < dptos.length; i++) {
		if(dptos[i]=='COCHABAMBA'){
			options.push('<option value="'+dptos[i]+'" selected>'+dptos[i]+'</option>');
		} else{
			options.push('<option value="'+dptos[i]+'">'+dptos[i]+'</option>');
		}
	};
	$('#inputDpto').html(options.join(''));
	$('#add').on({
		click:function(e){
			e.preventDefault();
			$(this).closest('.comunidades').append(tmpl(count));
			count += 1;
		}
	});//.css('color','#37abff');
	$('#del').on({
		click:function(e){
			e.preventDefault();
			if(count>=0){
				$(this).closest('.comunidades').children('.comunidad-'+(count-1)).remove()
				if(count>0){
					count -= 1;
				}
			}
		}
	});//.css('color','#ff7f35');
	$('form').on({
		submit:function(e){
			e.preventDefault();
			var o_form = $(this), btn_submit = $('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/municipios/nuevo_municipio',
				data = o_form.form2Dict(true),
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