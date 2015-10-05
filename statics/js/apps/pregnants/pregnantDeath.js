/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	$('#back, .back').on({
		click:function(e){
			e.preventDefault();
			//location.href='/embarazadas/gestion';
			location.href='/embarazos/gestion?id_per='+$('input[name=id_per]').val();
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
				'/embarazadas/defuncion',
				data = oform.form2Dict(),
				function(response){
					if(response){
						//location.href='/embarazadas/gestion';
						location.href='/embarazos/gestion?id_per='+$('input[name=id_per]').val();
					}
				}
			);
		}
	});
});