/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/redes_salud/gestion';
		}
	});
	var dptos = ['BENI', 'COCHABAMBA', 'CHUQUISACA', 'LA PAZ', 'ORURO', 'PANDO', 'POTOSÍ', 'SANTA CRÚZ', 'TARIJA'],
		options = [],
		count = 0,
		tmpl = function(n){
			return '<div class="row  municipio-'+n+'">'+
			'<div class="form-group has-feedback col-sm-5">'+
				'<label for="inputDpto">Departamento:</label>'+
				'<select name="dpto" id="inputDpto" class="form-control input-sm c_select" required="required"></select>'+
				'<span class="form-control-feedback"></span>'+
			'</div>'+
			'<div class="form-group has-feedback col-sm-7">'+
				'<label for="inputNombre">Nombre:</label>'+
				'<input type="text" name="nombre" id="inputNombre" class="form-control input-sm only_g_names" required>'+
				'<span class="form-control-feedback"></span>'+
			'</div></div>';
		};
	for (var i = 0; i < dptos.length; i++) {
		if(dptos[i]=='Cochamba'){
			options.push('<option value="'+dptos[i]+'" selected>'+dptos[i]+'</option>');
		} else{
			options.push('<option value="'+dptos[i]+'">'+dptos[i]+'</option>');
		}
	};
	$('#add').on({
		click:function(e){
			e.preventDefault();
			$(this).closest('.municipio').append(tmpl(count)).find('select').last().html(options.join('')).end().end();
			count += 1;
		}
	});//.css('color','#37abff');
	$('#del').on({
		click:function(e){
			e.preventDefault();
			if(count>=0){
				$(this).closest('.municipio').children('.municipio-'+(count-1)).remove();
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
				'/redes_salud/nueva_red',
				data = o_form.form2Dict(true),
				function(response){
					if(response){
						location.href='/redes_salud/gestion';
					} else{
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});