/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	$('#back, .back').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/gestion?id_per='+$('input[name=id_per]').val();
		}
	});
	$('#inputParto_prob').on({
		'click focusin':function(e){
			$(this).datetimepicker({
				locale: 'es',
				format: 'DD/MM/YYYY'
			});
		}
	}).inputmask({
		mask:'99/99/9999',
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this).form2Dict(), btn_submit = $('button[type=submit]');
			//console.log(oform);
			btn_submit.disable();
			$.post(
				'/embarazos/nuevo_embarazo',
				data = oform,
				function(response){
					if(response){
						location.href='/embarazos/gestion?id_per='+$('input[name=id_per]').val();
					} else{
						btn_submit.enable();
						$('input[name=parto_prob]').val('');
					}
				}
			);
		}
	});
});