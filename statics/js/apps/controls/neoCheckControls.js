/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	var o_key = $('#breadcrumbs').data('key');
	//console.log(o_key);
	$('#breadcrumbs').removeAttr('data-key');
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this);
			//console.log(oform.form2Dict());
			$.post(
				'/controles/control_asistencia',
				data = oform.form2Dict(),
				function(response){
					location.href='/controles/gestion?id_rcn='+o_key.id_rcn;
				}
			);
		}
	});
	$('#cancel, .backControl').on({
		click:function(e){
			e.preventDefault();
			location.href='/controles/gestion?id_rcn='+o_key.id_rcn;
		}
	});
	$('.backPregnant').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/gestion?id_per='+o_key.id_per;
		}
	});
});