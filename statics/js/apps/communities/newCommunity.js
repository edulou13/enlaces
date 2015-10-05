/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	var centros = ['1er. Nivel','2do. Nivel','3er. Nivel','Centro de Salud','Puesto de Salud'],
		options = [], count = 0,
		tmpl = function(n){
			return '<div class="row centro-'+n+'">'+
			'<div class="form-group has-feedback col-sm-5">'+
				'<label for="inputTipo">Tipo:</label>'+
				'<select name="tipo" id="inputTipo" class="form-control input-sm c_select" required></select>'+
				'<span class="form-control-feedback"></span>'+
			'</div>'+
			'<div class="form-group has-feedback col-sm-7">'+
				'<label for="inputNombre">Nombre:</label>'+
				'<input type="text" name="nombre" id="inputNombre" class="form-control input-sm only_g_names" required>'+
				'<span class="form-control-feedback"></span>'+
			'</div></div>';
		};
	for (var i = 0; i < centros.length; i++) {
		if(centros[i]=='Puesto de Salud'){
			options.push('<option value="'+centros[i]+'" selected>'+centros[i]+'</option>');
		} else{
			options.push('<option value="'+centros[i]+'">'+centros[i]+'</option>');
		}
	};
	$('#add').on({
		click:function(e){
			e.preventDefault();
			$(this).closest('.centros_salud').append(tmpl(count)).find('select').last().html(options.join('')).end().end();
			count += 1;
		}
	});//.css('color','#37abff');
	$('#del').on({
		click:function(e){
			e.preventDefault();
			if(count>=0){
				$(this).closest('.centros_salud').children('.centro-'+(count-1)).remove();
				if(count>0){
					count -= 1;
				}
			}
		}
	});//.css('color','#ff7f35');
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
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/comunidades/gestion?id_mup='+o_key.mup;
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			var oform = $(this), btn_submit = $('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/comunidades/nueva_comunidad',
				data = oform.form2Dict(true),
				function(response){
					if(response){
						location.href='/comunidades/gestion?id_mup='+o_key.mup;
					} else{
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});