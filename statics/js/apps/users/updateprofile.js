/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.user-profile').addClass('active');
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href = '/';
		}
	});
	var ci = $('input[name=ci]').val(), cellnumber = $('#cellphone').val(), login = $('input[name=login]').val();
	$('input[name=ci]').on({
		keyup:function(e){
			e.preventDefault();
			var o_ci = $(this), o_val = $(this).val(), chk_ptrn = $(this).data('pattern');
			if(o_val.match(chk_ptrn)){
				if(ci!=o_val){
					$.post(
						'/personas/v_ci',
						data = {'_xsrf':getCookie('_xsrf'), 'ci':o_val},
						function(response){
							if(response){
								swal({
									title: 'Error',
									text: o_val+', está registrado con otra persona!',
									type: 'error',
									confirmButtonText: "Continuar",
									confirmButtonClass: 'btn-primary'
								});
								o_ci.val(ci);
							}
						}
					);
				}
			}
		}
	});
	$('#cellphone').on({
		'keyup':function(e){
			e.preventDefault();
			var cellphone = $(this), o_val = $(this).val(), chk_ptrn = $(this).data('pattern');
			if(o_val.match(chk_ptrn)){
				if(cellnumber!=o_val){
					$.post(
						'/personas/v_userstelf',
						data = {'_xsrf':getCookie('_xsrf'),'telf':o_val},
						function(response){
							if(response){
								swal({
									title: 'Error',
									text: o_val+', está registrado con otra persona!',
									type: 'error',
									confirmButtonText: 'Continuar',
									confirmButtonClass: 'btn-primary'
								});
								cellphone.val(cellnumber);
							}
						}
					);
				}
			}
		}
	});
	$('input[name=login]').on({
		blur:function(e){
			e.preventDefault();
			var o_login = $(this), o_val = $(this).val(), chk_ptrn = $(this).data('pattern');
			if(o_val.match(chk_ptrn)){
				if(login!=o_val){
					$.post(
						'/usuarios/v_login',
						data = {'_xsrf':getCookie('_xsrf'), 'login':o_val},
						function(response){
							if(response){
								swal({
									title: 'Error',
									text: o_val+', está registrado con otro usuario!',
									type: 'error',
									confirmButtonText: 'Continuar',
									confirmButtonClass: 'btn-primary'
								});
							}
						}
					);
				}
			}
		}
	});
	$('form').on({
		submit:function(e){
			e.preventDefault();
			e.stopPropagation();
			var oform = $(this).form2Dict(), btn_submit = $('button[type=submit]');
			$.post(
				'/usuarios/profile',
				data = oform,
				function(response){
					if(response){
						location.href='/';
					} else{
						btn_submit.enable();
					}
				}
			);
		}
	});
});