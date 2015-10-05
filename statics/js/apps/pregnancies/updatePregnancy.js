/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	var o_key = $('#breadcrumbs').data('key');
	$('#breadcrumbs').removeAttr('data-key');
	// console.log(o_key);
	$('.pregnant-menu').addClass('active');
	$('.back_pregnant').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/gestion?id_per={0}'.format(o_key.id_per)
		}
	});
	$('#back, .back').on({
		click:function(e){
			e.preventDefault();
			location.href='/controles/gestion?id_emb={0}'.format(o_key.id_emb);
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
			var data = $(this).form2Dict(), btn_submit = $('button[type=submit]');
			btn_submit.disable();
			swal({
				title: 'Advertencia!', text:'Ésta acción es delicada, porque regenerará todos los registros vinculados a la Embarazada.',
				type:'warning', showCancelButton: true,
				cancelButtonText: 'Cancelar', cancelButtonClass: 'btn-default',
				confirmButtonText: 'Continuar', confirmButtonClass: 'btn-danger',
				closeOnConfirm: true
			}, function(){
				$.post(
					'/embarazos/reprogramar_embarazo',
					data = data,
					function(response){
						if(response){
							location.href='/controles/gestion?id_emb={0}'.format(o_key.id_emb);
						} else{
							btn_submit.enable();
						}
					}
				);
			});
			btn_submit.enable();
		}
	});
});