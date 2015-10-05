/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	$('#inputParto_inst').on({
		'click focusin':function(e){
			$(this).datetimepicker({
				locale: 'es',
				format: 'DD/MM/YYYY'
			});
		}
	}).inputmask({
		mask:'99/99/9999',
	});
	var count = 1, opreg = $('#breadcrumbs').data('key'),
		newborn_tmpl = function(numb){
			return '<hr class="newborn-'+numb+'">'+
			'<div class="row newborn-'+numb+'">'+
				'<fieldset class="form-group col-sm-6">'+
					'<label>Sexo:</label>'+
					'<select name="sexo'+numb+'" class="form-control input-sm c_select" required>'+
						'<option value="-1">-- Elija Uno --</option>'+
						'<option value="f">Femenino</option>'+
						'<option value="m">Masculino</option>'+
					'</select>'+
				'</fieldset>'+
				'<fieldset class="form-group has-feedback col-sm-6">'+
					'<label>Peso:</label>'+
					'<div class="input-group">'+
						'<span class="input-group-addon">Kilogramo</span>'+
						'<input type="text" name="peso" class="form-control input-sm only_neonato_weight" required>'+
						'<span class="form-control-feedback"></span>'+
					'</div>'+
				'</fieldset>'+
			'</div>'+
			'<div class="row newborn-'+numb+'">'+
			'<fieldset class="form-group has-feedback col-sm-5">'+
				'<label>Nombre(s):</label>'+
				'<input type="text" name="nombres" class="form-control input-sm only_p_names">'+
				'<span class="form-control-feedback"></span>'+
			'</fieldset>'+
			'<fieldset class="form-group has-feedback col-sm-7">'+
				'<label>Apellidos:</label>'+
				'<input type="text" name="apellidos" value="'+opreg.lastname+'" class="form-control input-sm only_p_lastnames">'+
				'<span class="form-control-feedback"></span>'+
			'</fieldset>'+
			'</div>';
		};
	$('#breadcrumbs').removeAttr('data-key');
	$('.del').disable();
	$('.add').on({
		click:function(e){
			e.preventDefault();
			$('.new_born').append(newborn_tmpl(count));
			count++;
			if(count==2){
				$('.del').enable();
			}
		}
	});
	$('.del').on({
		click:function(e){
			e.preventDefault();
			count = (count > -1)?(count-1):1;
			if(count <= 1){
				$(this).disable();
			}
			$('.new_born').find('.newborn-'+count).remove();
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this);
			//console.log(oform.form2Dict(true));
			$.post(
				'/embarazos/reg_parto',
				data = oform.form2Dict(true),
				function(response){
					if(response){
						location.href='/embarazos/gestion?id_per='+opreg.id;
					}
				}
			);
		}
	});
	$('#back, .back').on({
		click:function(e){
			e.preventDefault();
			//location.href='/embarazos/gestion?id_per='+opreg.id;
			location.href='/controles/gestion?id_emb='+opreg.id_emb;
		}
	});
	$('.pregnant').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazos/gestion?id_per='+opreg.id;
		}
	});
});