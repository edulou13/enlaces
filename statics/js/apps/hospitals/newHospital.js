/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .health-sub').addClass('active');
	var o_comunities = $('.key').data('key'),
		centros = ['Puesto de Salud','Centro de Salud','1er. Nivel','2do. Nivel','3er. Nivel'],
		options = [],
		tmpl = function(obj){
			return ''+
			'<div class="input-group">'+
				'<span class="input-group-addon">'+
					'<input type="checkbox" name="id_com" value="'+obj.id+'">'+
				'</span>'+
				'<label class="form-control input-sm">'+obj.nombre+'</label>'+
			'</div>';
		},
		prest = function(obj){
			return ''+
			'<div class="input-group">'+
				'<span class="input-group-addon">'+
					'<input type="checkbox" name="id_pst" value="'+obj.id_pst+'">'+
				'</span>'+
				'<label class="form-control input-sm">'+obj.nombre+'</label>'+
			'</div>';
		};
	for (var i = 0; i < centros.length; i++) {
		if(centros[i]=='Puesto de Salud'){
			options.push('<option value="'+centros[i]+'" selected>'+centros[i]+'</option>');
		} else{
			options.push('<option value="'+centros[i]+'">'+centros[i]+'</option>');
		}
	};
	$('#inputTipo').html(options.join(''));
	for (var i = 0; i < o_comunities.length; i++) {
		$('#comunidades').append(tmpl(o_comunities[i]));
	};
	$.post(
		'/prestaciones/disponibles',
		data = {'_xsrf':getCookie('_xsrf'), 'prestaciones': '[]'},
		function(response){
			if($.type(response)=='array'){
				for (var i = 0; i < response.length; i++) {
					$('#prestaciones').append(prest(response[i]));
				};
			}
		}
	);
	var o_key = $('.breadcrumb').data('key');
	//console.log(o_comunities, o_key);
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
			location.href='/centros_salud/gestion?id_com='+o_key.com;
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			o_form = $(this), btn_submit = $('button[type=submit]');
			btn_submit.disable();
			$.post(
				'/centros_salud/nuevo_establecimiento',
				data = o_form.form2Dict(true),
				function(response){
					if(response){
						location.href='/centros_salud/gestion?id_com={0}'.format(o_key.com);
					} else{
						btn_submit.enable();
					}
				}
			);
		}
	});
});