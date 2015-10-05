/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	$('#back, .back').on({click:function(e){e.preventDefault();location.href='/embarazos/gestion?id_per='+$('input[name=id_per]').val();}});
	$('input[name=f_nac]').on({
		'click focusin':function(e){
			$(this).datetimepicker({
				locale: 'es',
				format: 'DD/MM/YYYY'
			});
		}
	}).inputmask({
		mask:'99/99/9999',
	});
	var checkfields = $('form').data('key'),
		ldetnias = function(etnias){
			var options = [$('<option value="-1">-- Elija Una --</option>')];
			for (var i = 0; i < etnias.length; i++) {
				var etn = etnias[i], opt_etn = $('<option/>', {'value':etn.id_etn, 'text':etn.nombre});
				if(etn.id_etn==checkfields.id_etn){
					opt_etn.attr('selected',true);
				}
				options.push(opt_etn);
			}
			return options;
		},
		ldRedes = function(redes){
			var options = [$('<option value="-1">-- Elija Una --</option>')];
			for (var i = 0; i < redes.length; i++) {
				var red = redes[i], opt_red = $('<option/>', {'value':red.id_red, 'text':red.nombre}).data('municipios', red.municipios);
				if(checkfields.id_red==red.id_red){
					opt_red.attr('selected',true);
				}
				options.push(opt_red);
			}
			return options;
		},
		ldMunicipios = function(municipios){
			var options = [$('<option value="-1">-- Elija Uno --</option>')];
			for (var i = 0; i < municipios.length; i++) {
				var mup = municipios[i], opt_mup = $('<option/>', {'value':mup.id_mup, 'text':mup.nombre}).data('comunidades', mup.comunidades);
				if(checkfields.id_mup==mup.id_mup){
					opt_mup.attr('selected',true);
				}
				options.push(opt_mup);
			}
			return options;
		},
		ldComunidades = function(comunidades){
			var options = [$('<option value="-1">-- Elija Uno --</option>')];
			for (var i = 0; i < comunidades.length; i++) {
				var com = comunidades[i], opt_com = $('<option/>', {'value':com.id_com, 'text':com.nombre}).data('centros', com.centros_salud);
				if(checkfields.id_com==com.id_com){
					opt_com.attr('selected',true);
				}
				options.push(opt_com);
			}
			return options;
		},
		ldCentros = function(centros){
			var options = [$('<option/>', {'value':-1, 'text':'-- Elija Uno --'})];
			for (var i = 0; i < centros.length; i++) {
				var cen = centros[i], opt_cen = $('<option/>', {'value':cen.id_cen, 'text':cen.nombre});
				if(checkfields.centro_salud==cen.id_cen){
					opt_cen.attr('selected', true);
				}
				options.push(opt_cen);
			};
			return options;
		};
	if(checkfields.is_pregnant){
		$.post(
			'/etnias/disponibles',
			data = {'_xsrf':getCookie('_xsrf')},
			function(response){
				$('#etnia').html(ldetnias(response));
			}
		);
		$.post(
			'/redes_salud/geografia',
			data = {'_xsrf':$('input[name=_xsrf]').val()},
			function(response){
				$('#red').html(ldRedes(response)).on({
					change:function(){
						var o_val = +$(this).val(), municipios = $(this).find('option[value="'+o_val+'"]').data('municipios');
						if(o_val>0){
							$('#municipio').html(ldMunicipios(municipios)).on({
								change:function(){
									var o_val = +$(this).val();
									if(o_val>0){
										comunidades = $(this).find('option[value="'+o_val+'"]').data('comunidades');
										$('#comunidad').html(ldComunidades(comunidades)).on({
											change:function(){
												var o_val = +$(this).val();
												if(o_val>0){
													centros = $(this).find('option[value="'+o_val+'"]').data('centros');
													$('#centro').html(ldCentros(centros));
												} else{
													$('centro').html('<option value="-1">-- Elija Una --</option>');
												}
											}
										}).change();
									} else{
										$('#comunidad').html('<option value="-1">-- Elija Una --</option>');
										$('#centro').html('<option value="-1">-- Elija Una --</option>');
									}
								}
							}).change();
						} else{
							$('#municipio').html('<option value="-1">-- Elija Uno --</option>');
							$('#comunidad').html('<option value="-1">-- Elija Una --</option>');
							$('#centro').html('<option value="-1">-- Elija Una --</option>');
						}
					}
				}).change();
			}
		);
	} else{
		$('.locations').disable().hide();
	}
	var pregnant_telf = +$('input[name=telf]').val(), contact_telf = $('input[name=c_telf]').val(), current_ci = $('input[name=ci]').val(),
		c_id_per = $('input[name=c_id_per]').val(), c_names = $('input[name=c_nombres]').val(), c_lastnames = $('input[name=c_apellidos]').val(), c_sexo = $('select[name=c_sexo]').val();
	$('input[name=telf]').on({
		blur:function(e){
			var o_telf = $(this), o_val = $(this).val();
			if(pregnant_telf != +o_val && o_val.length==8 && o_val.match(o_telf.data('pattern'))){
				if(o_val != contact_telf){
					$.post(
						'/personas/v_telf',
						data = {'_xsrf':$('input[name=_xsrf]').val(), 'telf':o_val},
						function(response){
							//console.log(response);
							if(response){
								o_telf.val(pregnant_telf).focus().closest('.form-group').removeClass('has-success has-error');
								swal({
									title: 'Error!',
									text: 'El nro. '+o_val+', está registrado!.\nPor favor use otro.',
									type: 'error',
									confirmButtonText: 'Continuar',
								});
							}
						}
					);
				} else{
					o_telf.val(pregnant_telf).focus().closest('.form-group').removeClass('has-success has-error');
				}
			}
		}
	});
	$('input[name=c_telf]').on({
		keyup:function(e){
			var o_telf = $(this), o_val = o_telf.val();
			$('input[name=c_id_per]').enable().val(c_id_per);
			if(o_val.length==8 && o_val!=contact_telf && o_val.match(o_telf.data('pattern'))){
				if(o_val!=pregnant_telf){
					$('form').find('.optional').enable().show();
					swal({
						title: 'Advertencia!',
						text: 'Desea cambiar de contacto?',
						type: 'warning',
						showCancelButton: true,
						cancelButtonText: "Cancelar",
						//confirmButtonColor: "#d9534f",
						confirmButtonText: "Cambiar",
						closeOnConfirm: true
					}, function(){
						$('form').find('.optional').show().end().find('.contact-name').text('Contacto');
						$.post(
							'/personas/v_telf',
							data = {'_xsrf':$('input[name=_xsrf]').val(), 'telf':o_val},
							function(response){
								//console.log(response);
								if(response){
									//o_telf.val(contact_telf).focus().closest('.form-group').removeClass('has-success has-error');
									$.post(
										'/personas/getbycellphone',
										data = {'_xsrf':getCookie('_xsrf'),'telf':o_val},
										function(contact){
											c_id_per = contact.id_per;
											c_names = contact.nombres;
											c_lastnames = contact.apellidos;
											$('input[name=c_nombres]').val(contact.nombres);
											$('input[name=c_apellidos]').val(contact.apellidos);
											$('input[name=c_id_per]').enable().val(contact.id_per);
											$('form').find('.optional').disable().hide().end().find('.contact-name').text(contact.persona);
											$('select[name=c_sexo]').find('option:selected').removeAttr('selected').end().find('option[value="'+contact.sexo+'"]').attr('selected',true).select();
										}
									);
								} else{
									$('input[name=c_id_per]').disable();
									$('form').find('.optional').enable().show();
									$('input[name=c_nombres], input[name=c_apellidos]').val('');
									$('select[name=c_sexo]').find('option:selected').removeAttr('selected').end().find('option[value="-1"]').attr('selected',true).select();
								}
							}
						);
					});
				} else{
					$('form').find('.optional').enable().show().end().find('.contact-name').text('Contacto');
					o_telf.val(contact_telf).focus().closest('.form-group').removeClass('has-success has-error').find('span').removeClass('fa-check fa-times');
					swal({
						title: 'Error!',
						text: 'El nro. de contacto, no puede ser igual al de la embarazada!.\nPor favor elija otro.',
						type: 'error',
						confirmButtonText: 'Continuar',
					});
				}
			} else{
				if(o_val.length==8){
					o_telf.val(contact_telf).closest('.form-group').removeClass('has-success has-error').find('span').removeClass('fa-check fa-times');
					$('input[name=c_id_per]').enable();
					$('form').find('.optional').enable().show().end().find('.contact-name').text('Contacto');
					$('input[name=c_nombres]').val(c_names);
					$('input[name=c_apellidos]').val(c_lastnames);
					$('select[name=c_sexo]').find('option:selected').removeAttr('selected').end().find('option[value="'+c_sexo+'"]').attr('selected',true).select();
				} else{
					o_telf.closest('.form-group').removeClass('has-success').addClass('has-error').find('span').removeClass('fa-check').addClass('fa-times');
				}
			}
		}
	});
	current_ci = current_ci.length==8?current_ci:'';
	$('input[name=ci]').on({
		blur:function(e){
			var o_ci = $(this), ci_val = $(this).val();
			if(ci_val.length>=7 && ci_val.length<=8 && ci_val!=current_ci){
				$.post(
					'/personas/v_ci',
					data = {'_xsrf':getCookie('_xsrf'),'ci':o_ci.val()},
					function(response){
						if(response){
							o_ci.val(current_ci).focus().closest('.form-group').removeClass("has-success has-error");
							swal({
								title: 'Error!',
								text: 'El CI: '+ci_val+', está registrado!.\nPor favor use otro.',
								type: 'error',
								confirmButtonText: 'Continuar',
							});
						} else{
							o_ci.closest('.form-group').removeClass("has-error").addClass("has-success").find('span').removeClass('fa-times').addClass('fa fa-check');
						}
					}
				);
			}
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this), btn_submit = $(this).find('button[type=submit]');
			btn_submit.disable().hide();
			$.post(
				'/embarazadas/modificar_embarazada',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/embarazos/gestion?id_per='+$('input[name=id_per]').val();
					} else{
						btn_submit.enable().show();
						var o_telf = $('input[name=c_telf]');
						$.post(
							'/personas/v_telf',
							data = {'_xsrf':$('input[name=_xsrf]').val(), 'telf':o_telf.val()},
							function(response){
								if(response){
									swal({
										title: 'Error!',
										text: 'El nro. '+o_telf.val()+', está registrado!.\nPor favor elija otro.',
										type: 'error',
										confirmButtonText: 'Continuar',
										closeOnConfirm: true,
									});
									o_telf.val(contact_telf);
								}
							}
						);
					}
				}
			);
		}
	});
});