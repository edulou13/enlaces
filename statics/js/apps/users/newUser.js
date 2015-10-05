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
	var rol = $('#inputRol'), alcance = rol.closest('.form-group').next(), redes_salud = $('.redes_salud'), municipios = $('.municipios'), centros_salud = $('.centros_salud'),
		/*
		tipo_tmpl = function(obj){
			var options = ['<option value="-1">-- Elija Uno --</option>'];
			for (var i = 0; i < obj.length; i++) {
				options.push('<option value="'+obj[i].id_tip+'">'+obj[i].nombre+'</option>');
			}
			return options.length>1?options.join(''):'<option value="-1">-- Sin Tipos --</option>';
		},
		*/
		redes_tmpl = function(redes){
			var options = [$('<option/>',{'value':-1,'text':'-- Elija Una --'})];
			for (var i = 0; i < redes.length; i++) {
				var ored = redes[i],
					t_opt = $('<option/>',{'value':ored.id_red,'text':ored.nombre}).data({'municipios':ored.municipios,'centros':ored.centros});
				options.push(t_opt);
			}
			return options.length>1?options:[$('<option/>',{'value':-1,'text':'-- Sin Redes de Salud --'})];
		},
		mups_tmpl = function(municipios){
			var options = [$('<option/>',{'value':-1,'text':'-- Elija Uno --'})];
			for (var i = 0; i < municipios.length; i++) {
				var omup = municipios[i], t_opt = $('<option/>',{'value':omup.id_mup,'text':omup.nombre});
				options.push(t_opt);
			}
			return options.length>1?options:[$('<option/>',{'value':-1,'text':'-- Sin Municipios --'})];
		},
		centros_tmpl = function(centros){
			var options = [$('<option/>',{'value':-1,'text':'-- Elija Uno --'})];
			for (var i = 0; i < centros.length; i++) {
				var ocen = centros[i], t_opt = $('<option/>',{'value':ocen.id_cen,'text':ocen.nombre});
				options.push(t_opt);
			}
			return options.length>1?options:[$('<option/>',{'value':-1,'text':'-- Sin Establecimientos --'})];
		};
	alcance.disable().hide();
	redes_salud.disable().hide();
	municipios.disable().hide();
	centros_salud.disable().hide();
	/*
	$.post(
		'/tipos/disponibles',
		data = {'_xsrf':getCookie('_xsrf')},
		function(response){
			if($.type(response)=='array'){
				$('#inputTipo').html(tipo_tmpl(response));
			}
		}
	);*/
	$.post(
		'/redes_salud/disponibles',
		data = {'_xsrf':getCookie('_xsrf')},
		function(response){
			if($.type(response)=='array'){
				redes_salud.find('select').html(redes_tmpl(response));
			}
		}
	);
	$('#inputLogin').on({
		'blur':function(e){
			var o_val = $(this).val(), o_login = $(this);
			if(o_val.length>5){
				$.post(
					'/usuarios/v_login',
					data = {'_xsrf':getCookie('_xsrf'),'login':o_val},
					function(response){
						if(response){
							$('button[type=submit]').disable();
							o_login.val('').focus().closest('.form-group').removeClass("has-success").addClass("has-error").find('span').removeClass('fa-check').addClass('fa fa-time');
							swal({
								title: 'Error!',
								text: '"'+o_val+'", no está disponible!.\nPor favor elija otro.',
								type: 'error',
								confirmButtonText: 'Continuar',
								closeOnConfirm: false
							});
						} else{
							$('button[type=submit]').enable();
							o_login.closest('.form-group').removeClass("has-error fail-check").addClass("has-success").find('span').removeClass('fa-times').addClass('fa fa-check');
						}
					}
				);
			}/*
			else if(o_val.length==0){
				o_login.attr({'placeholder':'Campo obligatorio'});
				//$('button[type=submit]').disable();
			}*/
		}
	});
	$('#inputTelf').on({
		'blur':function(e){
			var o_val = $(this).val(), o_telf = $(this);
			if(o_val.length==8){
				$.post(
					'/personas/v_userstelf',
					data = {'_xsrf':getCookie('_xsrf'),'telf':o_val},
					function(response){
						//console.log('check: '+response);
						$('form').find('.optional').each(function(){
							$(this).enable().show();
						});
						if(response==null){
							//o_telf.focus().closest('.form-group').removeClass("has-success").addClass("fail-check has-error").find('span').removeClass('fa-check').addClass('fa fa-time');
							o_telf.val('').focus().closest('.form-group').removeClass("has-success").addClass("has-error").find('span').removeClass('fa-check').addClass('fa fa-time');
							swal({
								title: 'Error!',
								text: 'El nro. '+o_val+', está registrado!.\nPor favor use otro.',
								type: 'error',
								confirmButtonText: 'Continuar',
								closeOnConfirm: false
							});
						} else if(response==true){
							o_telf.closest('.form-group').removeClass("has-error").addClass("has-success").find('span').removeClass('fa-times').addClass('fa fa-check');
							$.post(
								'/personas/getbycellphone',
								data = {'_xsrf':getCookie('_xsrf'),'telf':o_val},
								function(person){
									$('form').find('.person').text(person.persona).end().find('.optional').each(function(){
										$(this).disable().hide();
									});
								}
							);
						} else{
							o_telf.closest('.form-group').removeClass("has-error").addClass("has-success").find('span').removeClass('fa-times').addClass('fa fa-check');
						}
					}
				);
			}
			else if(o_val.length>0 && o_val.length<8){
				o_telf.focus().val('');
			}
			else if(o_val.length==0){
				o_telf.focus().val('');
			}
		}
	});
$('input[name=ci]').on({
	blur:function(e){
		var o_ci = $(this), ci_val = $(this).val();
		if(ci_val.length>=7 && ci_val.length<=8){
			$.post(
				'/personas/v_ci',
				data = {'_xsrf':getCookie('_xsrf'),'ci':o_ci.val()},
				function(response){
					if(response){
						o_ci.val('').focus().closest('.form-group').removeClass("has-success").addClass("has-error").find('span').removeClass('fa-check').addClass('fa fa-time');
						swal({
							title: 'Error!',
							text: 'El CI: '+ci_val+', está registrado!.\nPor favor use otro.',
							type: 'error',
							confirmButtonText: 'Continuar',
							closeOnConfirm: false
						});
					} else{
						o_ci.closest('.form-group').removeClass("has-error").addClass("has-success").find('span').removeClass('fa-times').addClass('fa fa-check');
					}
				}
			);
		}
	}
});
	rol.on({
		change:function(e){
			//console.log($(this).val()!='Administrador');
			if($(this).val()!='Administrador'){
				alcance.enable().show();
			} else{
				alcance.find('option[value="1"]').attr('selected',true).end().disable().hide();
				redes_salud.find('select').find('option[value="-1"]').attr('selected',true).end().end().disable().hide();
				municipios.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
				centros_salud.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
			}
		}
	});
	alcance.find('select').on({
		change:function(e){
			var o_val = +$(this).val();
			redes_salud.find('select').find('option[value="-1"]').attr('selected',true).end().end().disable().hide();
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
			var o_val = +$(this).val(), o_al = +alcance.find('select').val(), option = $(this).find('option:selected');
			municipios.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
			centros_salud.find('select').html('<option value="-1">-- Elija Uno --</option>').end().disable().hide();
			if(o_val != -1 && o_al == 3){
				municipios.find('select').html(mups_tmpl(option.data('municipios'))).end().enable().show();
			}
			else if(o_val != -1 && o_al == 4){
				centros_salud.find('select').html(centros_tmpl(option.data('centros'))).end().enable().show();
			}
		}
	});
	var oform =  $('form'), btn_submit = $('button[type=submit]');
	oform.on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			btn_submit.disable().hide();
			$.post(
				'/usuarios/nuevo_usuario',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/usuarios/gestion';
					} else{
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});