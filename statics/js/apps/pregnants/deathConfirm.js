/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	var o_key = $('.big-form').data('key'), btn_submit = $('button[type=submit]'), btn_interr = $('#interr');
	//console.log('conf',o_key);
	$('.big-form').removeAttr('data-key');
	$('#back, .back').on({
		click:function(e){
			e.preventDefault();
			//location.href='/embarazadas/gestion';
			location.href='/embarazos/gestion?id_per='+o_key.id_per;
		}
	});
	$('.optional').disable();
	$('input[name=f_conf]').on({
		'click focusin':function(e){
			$(this).datetimepicker({
				locale: 'es',
				format: 'DD/MM/YYYY'
			});
		}
	}).inputmask({
		mask:'99/99/9999',
	});
	$('#interr').on({
		click:function(e){
			e.preventDefault();
			btn_submit.disable().hide();
			btn_interr.disable().hide();
			$.post(
				'/embarazadas/del_defuncion',
				data = {'_xsrf':getCookie('_xsrf'),'id_def':o_key.id_def},
				function(response){
					if(!response){
						location.href='/embarazadas/gestion?id_per='+o_key.id_per;
					} else{
						btn_submit.enable().show();
						btn_interr.enable().show();
					}
				}
			);
		}
	});
	if(o_key.done){
		$('.right-side').disable();
	}
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this);
			btn_submit.disable().hide();
			btn_interr.disable().hide();
			$.post(
				'/embarazadas/conf_defuncion',
				data = oform.form2Dict(),
				function(response){
					if(response){
						//location.href='/embarazadas/gestion';
						location.href='/embarazos/gestion?id_per='+o_key.id_per;
					} else{
						btn_submit.enable().show();
					}
				}
			);
		}
	});
});