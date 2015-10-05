/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	var o_key = $("#breadcrumbs").data('key');
	$('#breadcrumbs').removeAttr('data-key');
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
	$('.optional').disable().hide();
	$('.yes, .no').on({
		click:function(e){
			var oconf = $(this);
			if(+oconf.val()==1){
				$('.no').removeAttr('checked');
				$('.optional').enable().show();
			} else{
				$('.yes').removeAttr('checked');
				$('.optional').disable().hide();
			}
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this);
			//console.log($(this).form2Dict());
			$.post(
				'/embarazos/interrumpir',
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