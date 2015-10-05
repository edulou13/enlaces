/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	var o_key = $('#breadcrumbs').data('key');
	$('#breadcrumbs').removeAttr('data-key');
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/controles/gestion?id_rcn='+o_key.id_rcn;
		}
	});
	$('input[name=fecha], input[name=f_notf], input[name=f_conf]').on({
		'click focusin':function(e){
			$(this).datetimepicker({
				locale:'es',
				format: 'DD/MM/YYYY'
			});
		}
	}).inputmask({
		mask:'99/99/9999',
	});
	$('.delete').on({
		click:function(e){
			e.preventDefault();
			$.post(
				'/controles/eliminar_defuncion',
				data = {'_xsrf':getCookie('_xsrf'),'id_def':o_key.id_def},
				function(response){
					if(!response){
						location.href='/controles/gestion?id_rcn='+o_key.id_rcn;
					}
				}
			);
		}
	});
	$('.optional').disable();
	if(o_key.done){
		$('form').find(':input:not(button)').disable().removeAttr('name');
	} else{
		$('form').on({
			submit:function(e){
				e.preventDefault();
				var oform = $(this), btn_submit = $('button[type=submit]');
				btn_submit.disable().hide();
				$.post(
					'/controles/neo_confirmDef',
					data = oform.form2Dict(),
					function(response){
						if(response){
							location.href='/controles/gestion?id_rcn='+o_key.id_rcn;
						} else{
							btn_submit.enable().show();
						}
					}
				);
			}
		});
	}
});