/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.manager-menu, .user-sub').addClass('active');
	$('#cancel, .back').on({
		click:function(e){
			e.preventDefault();
			location.href='/usuarios/gestion';
		}
	});
	var o_user = $('.key').data('key'), btn_submit = $('button[type=submit]'), btn_del = $('#del');
	$('.key').removeAttr('data-key');
	//console.log(o_user);
	var rol = $('#inputRol'), alcance = rol.closest('.form-group').next(), redes_salud = $('.redes_salud'), municipios = $('.municipios'), centros_salud = $('.centros_salud'),
		o_redes_salud=[],
		tipo_tmpl = function(obj){
			var options = ['<option value="-1">-- Elija Uno --</option>'];
			for (var i = 0; i < obj.length; i++) {
				options.push('<option value="'+obj[i].id_tip+'">'+obj[i].nombre+'</option>');
			}
			return options.length>1?options.join(''):'<option value="-1">-- Sin Tipos --</option>';
		},
		redes_tmpl = function(){
			var options = ['<option value="-1">-- Elija Una --</option>'], f_red = (+o_user.red_salud>0?+o_user.red_salud:+o_user.red);
			for (var i = 0; i < o_redes_salud.length; i++) {
				var obj = o_redes_salud[i];
				options.push('<option value="'+obj.id_red+'"'+(f_red==obj.id_red?" selected":"")+'>'+obj.nombre+'</option>');
			}
			return options.length>1?options.join(''):'<option value="-1">-- Sin Redes de Salud --</option>';
		},
		mups_tmpl = function(pk){
			var options = ['<option value="-1">-- Elija Uno --</option>'];
			for (var i = 0; i < o_redes_salud.length; i++) {
				//console.log('pk: '+pk+' id_red: '+o_redes_salud[i].id_red+' equal: '+(o_redes_salud[i].id_red==pk));
				//console.log('pk: '+$.type(pk)+' id_red: '+$.type(o_redes_salud[i].id_red));
				var red = o_redes_salud[i];
				if(red.id_red==pk && red.municipios.length>0){
					var mups_list = o_redes_salud[i].municipios;
					for (var j = 0; j < mups_list.length; j++) {
						var obj = mups_list[j];
						options.push('<option value="'+obj.id_mup+'"'+(+o_user.municipio>0&&+o_user.municipio==obj.id_mup?" selected":"")+'>'+obj.nombre+'</option>');
					}
					break;
				}
			}
			return options.length>1?options.join(''):'<option value="-1">-- Sin Municipios --</option>';
		},
		centros_tmpl = function(pk){
			var options = ['<option value="-1">-- Elija Uno -- </option>'];
			for (var i = 0; i < o_redes_salud.length; i++) {
				var red = o_redes_salud[i];
				if(red.id_red==pk && red.centros.length>0){
					var centros_list = o_redes_salud[i].centros;
					for (var j = 0; j < centros_list.length; j++) {
						var obj = centros_list[j];
						options.push('<option value="'+obj.id_cen+'"'+(+o_user.centro_salud>0&&+o_user.centro_salud==obj.id_cen?" selected":"")+'>'+obj.nombre+'</option>');
					}
					break;
				}
			}
			return options.length>1?options.join(''):'<option value="-1">-- Sin Establecimientos --</option>';
		};
	/*
	$.post(
		'/tipos/disponibles',
		data = {'_xsrf':getCookie('_xsrf')},
		function(response){
			if($.type(response)=='array'){
				$('#inputTipo').html(tipo_tmpl(response));
			}
		}
	);
	*/
	$.post(
		'/redes_salud/disponibles',
		data = {'_xsrf':getCookie('_xsrf')},
		function(response){
			if($.type(response)=='array'){
				o_redes_salud = response;
				redes_salud.find('select').html(redes_tmpl());
				load_user_options();
			}
		}
	);
	var current_account = $('#inputLogin').val();
	$('#inputLogin').on({
		'blur':function(e){
			var o_val = $(this).val(), o_login = $(this);
			if(o_val.length>5 && o_user.login!=o_val){
				$.post(
					'/usuarios/v_login',
					data = {'_xsrf':getCookie('_xsrf'),'login':o_val},
					function(response){
						if(response){
							o_login.val(current_account).focus().closest('.form-group').removeClass("has-success").addClass("has-error");
							swal({
								title: 'Error!',
								text: '"'+o_val+'", no está disponible!.\nPor favor escoja otro.',
								type: 'error',
								confirmButtonText: 'Continuar',
								closeOnConfirm: false
							});
						} else{
							o_login.closest('.form-group').removeClass("has-error").addClass("has-success");
							$('button[type=submit]').enable();
						}
					}
				);
			}
			else if(o_val.length==0){
				o_login.attr({'placeholder':'Debe llenar éste campo..!'});
				//$('button[type=submit]').disable();
			}
		}
	});
	/*
	$('#inputTelf').on({
		'blur':function(e){
			var o_val = $(this).val(), o_telf = $(this);
			if(o_val.length==8){
				$.post(
					'/personas/v_telf',
					data = {'_xsrf':getCookie('_xsrf'),'telf':o_val},
					function(response){
						if(response){
							o_telf.focus().closest('.form-group').removeClass("has-success").addClass("has-error");
						} else{
							o_telf.closest('.form-group').removeClass("has-error").addClass("has-success");
						}
					}
				);
			}
			else if(o_val.length>0 && o_val.length<8){
				o_telf.focus().attr({'placeholder':'No es un nro. celular..!'});
			}
			else if(o_val.length==0){
				o_telf.focus().attr({'placeholder':'Éste es un campo obligatorio'});
			}
		}
	});*/
	rol.on({
		change:function(e){
			if($(this).val()!='Administrador'){
				alcance.enable().show();
			} else{
				alcance.disable().hide();
				redes_salud.find('select').html(redes_tmpl(o_redes_salud)).end().disable().hide();
				municipios.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
				centros_salud.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
			}
		}
	});
	alcance.find('select').on({
		change:function(e){
			var o_val = +$(this).val();
			redes_salud.find('select').html(redes_tmpl(o_redes_salud)).end().disable().hide();
			municipios.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
			centros_salud.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
			if(o_val==2){
				redes_salud.enable().show();
			}
			else if(o_val==3){
				redes_salud.enable().show();
				municipios.enable().show();
			}
			else if(o_val==4){
				redes_salud.enable().show();
				centros_salud.enable().show();
			}
		}
	});
	redes_salud.find('select').on({
		change:function(e){
			var o_val = +$(this).val(), o_al = +alcance.find('select').val();
			municipios.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
			centros_salud.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
			if(o_val != -1 && o_al == 3){
				municipios.find('select').html(mups_tmpl(o_val)).end().enable().show();
			}
			else if(o_val != -1 && o_al == 4){
				centros_salud.find('select').html(centros_tmpl(o_val)).end().enable().show();
			}
		}
	});
	var load_user_options = function(){
		if(+o_user.alcance<1){
			alcance.disable().hide();
			redes_salud.disable().hide();
		} else{
			if(+o_user.alcance>1){
				alcance.find('select').find('option[value="'+o_user.alcance+'"]').attr('selected',true).end();
				var o_val = (+o_user.red_salud>0?+o_user.red_salud:+o_user.red), o_al = +o_user.alcance;
				//console.log(o_val, o_al);
				redes_salud.enable().show();
				if(o_val != -1 && o_al == 3){
					municipios.find('select').html(mups_tmpl(o_val)).end().enable().show();
				}
				else if(o_val != -1 && o_al == 4){
					centros_salud.find('select').html(centros_tmpl(o_val)).end().enable().show();
				}
			} else{
				redes_salud.disable().hide();
			}
		}
		if(+o_user.municipio<1){
			municipios.disable().hide();
		}
		if(+o_user.centro_salud<1){
			centros_salud.disable().hide();
		}
	};
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this);
			btn_submit.disable().hide();
			btn_del.disable().hide();
			$.post(
				'/usuarios/modificar_usuario',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/usuarios/gestion';
					} else{
						btn_submit.enable().show();
						btn_del.enable().show();
					}
				}
			);
		}
	});
	btn_del.on({
		click:function(e){
			e.preventDefault();
			btn_submit.disable().hide();
			btn_del.disable().hide();
			$.post(
				'/usuarios/eliminar_usuario',
				data = {'_xsrf':getCookie('_xsrf'),'persona':$('input[name=persona]').val()},
				function(response){
					if(response==false){
						location.href='/usuarios/gestion';
					} else{
						btn_submit.enable().show();
						btn_del.enable().show();
					}
				}
			);
		}
	});
});