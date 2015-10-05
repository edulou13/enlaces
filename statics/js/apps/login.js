/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	var alertbox = $('.alert-Box').clone();
	$('.alert-Box').html('');
	$('input[name=login]').focus();
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this), btn_submit = $('button[type=submit]');
			btn_submit.disable();
			$.post(
				'/login',
				data = oform.form2Dict(),
				function(response){
					if(response){
						location.href='/';
					} else{
						btn_submit.enable();
						$('input').tooltip('hide');
						$('.alert-Box').html(alertbox.html()).find('#alertLogin').show();
					}
				}
			);
		}
	});
});