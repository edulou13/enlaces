/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	var o_key = $('#breadcrumbs').data('key');
	$('#breadcrumbs').removeAttr('data-key');
	//console.log(o_key);
	$('.message-menu, .sms-catalog').addClass('active');
	$('#back, .back').on({
		click:function(e){
			e.preventDefault();
			location.href='/mensajes/gestion';
		}
	});
	var nro_control = $('input[name=nro_control]'), prtn = nro_control.closest('.form-group'), feedback = $(prtn).find('.form-control-feedback');
	nro_control.attr({readonly:true});
	$('#tipo').on({
		change:function(e){
			var oval = +$(this).val();
			nro_control.val('');
			prtn.removeClass('has-success has-error');
			feedback.removeClass('fa-check fa-times');
			if(oval != -1){
				$.post(
					'/mensajes/before_save',
					data = {'_xsrf':getCookie('_xsrf'), 'tipo': oval},
					function(response){
						if(response != -1){
							nro_control.val(response);
						}
					}
				);
				nro_control.attr('name','nro_control').removeClass('only_g_names').addClass('only_msg_number').prev().text('Nro. de Control:').end();
			}
			/*
			if(oval==6){
				nro_control.attr('name','titulo').removeClass('only_msg_number').addClass('only_g_names').prev().text('Título:').end();
			}*/
		}
	});
	$('.fileinput').fileinput();
	var oaudio = $('input[name=audio]');
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this), cedesform = new FormData(), btn_submit = $('button[type=submit]');
			//console.log(oaudio[0].files[0]);
			btn_submit.disable().hide();
			if(oaudio.val().length){
				$.post(
					'/mensajes/adicionar_msj',
					data = oform.form2Dict(),
					function(response){
						if(response.status==true){
							cedesform.append('tipo', data.tipo);
							cedesform.append('nro', data.nro_control);
							cedesform.append('audio', oaudio[0].files[0]);
							cedesform.append('audioname', response.audio)
							$.ajax({
								//url: 'http://200.87.44.218:8000/getaudiofile',
								url: 'http://{0}:{1}/getaudiofile'.format(o_key.host, o_key.port),
								type: 'POST',
								data:  cedesform,
								mimeType:"multipart/form-data",
								contentType: false,
								cache: false,
								processData:false,
								success: function(resp){
									if(resp){
										location.href='/mensajes/gestion';
									} else{
										prtn.removeClass('has-success').addClass('has-error');
										feedback.removeClass('fa-check').addClass('fa-times');
										btn_submit.enable().show();
									}
								}
							});
						} else{
							prtn.removeClass('has-success').addClass('has-error');
							feedback.removeClass('fa-check').addClass('fa-times');
							btn_submit.enable().show();
						}
					}
				);
			} else {
				btn_submit.enable().show();
			}
		}
	});
});