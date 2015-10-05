/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	var o_key = $("#breadcrumbs").data('key'), btn_submit = $('button[type=submit]'), btn_interr = $('#interr');
	$("#breadcrumbs").removeAttr('data-key');
	$('input[name=f_conf]').on({
		'click focusin':function(e){
			$(this).datetimepicker({
				locale:'es',
				format: 'DD/MM/YYYY'
			});
		}
	}).inputmask({
		mask:'99/99/9999',
	});
	$('.optional').disable();
	if(o_key.done){
		$('.right-side').disable();
	}
	$('#interr').on({
		click:function(e){
			e.preventDefault();
			btn_submit.disable().hide();
			btn_interr.disable().hide();
			$.post(
				'/embarazos/del_interr',
				data = {'_xsrf':getCookie('_xsrf'),'id_def':$('input[name=id_def]').val()},
				function(response){
					if(!response){
						location.href='/controles/gestion?id_emb='+o_key.id_emb;
					} else{
						btn_submit.enable().show();
						btn_interr.enable().show();
					}
				}
			);
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this);
			//console.log($(this).form2Dict());
			$.post(
				'/embarazos/conf_interr',
				data = oform.form2Dict(),
				function(response){
					if(response){
						//location.href='/embarazadas/gestion';
						location.href='/controles/gestion?id_emb='+o_key.id_emb;
					}
				}
			);
		}
	});
	$('.pregnant').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/gestion?id_per='+o_key.id_per;
		}
	});
	$('#back, .back').on({
		click:function(e){
			e.preventDefault();
			//location.href='/embarazadas/gestion';
			location.href='/controles/gestion?id_emb='+o_key.id_emb;
		}
	});
});