/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$('.pregnant-menu').addClass('active');
	var o_key = $('#breadcrumbs').data('key');
	$('.back').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazadas/gestion';
		}
	});
	$('.edit').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazadas/modificar_embarazada?id_per='+o_key;
		}
	});
	$('.pregnancy').on({
		click:function(e){
			e.preventDefault();
			location.href="/embarazos/nuevo_embarazo?id_per="+o_key;
		}
	});
	$('.confirm').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazadas/conf_defuncion?id_per='+o_key;
		}
	});
	$('.death_reg').on({
		click:function(e){
			e.preventDefault();
			location.href='/embarazadas/defuncion?id_per='+o_key;
		}
	});
	$('.pregDisable').on({
		click:function(e){
			e.preventDefault();
			swal({
				title: 'Advertencia!', text: 'Está seguro?',
				type: 'warning', showCancelButton: true,
				cancelButtonText: "Cancelar", cancelButtonClass: 'btn-warning',
				confirmButtonText: "Confirmar", confirmButtonClass: 'btn-primary',
				closeOnConfirm: true
			}, function(){
				$.post(
					'/embarazadas/eliminar',
					data = {'_xsrf':getCookie('_xsrf'),'id_per':o_key},
					function(response){
						if(!response){
							location.href='/embarazos/gestion?id_per='+o_key;
						}
					}
				);
			});
		}
	});
	var strWindowFeatures = 'menubar=no,location=no,resizable=yes,scrollbars=yes,status=no,replace=true';
	$('.logs').on({
		click:function(e){
			e.preventDefault();
			var btn_logs = $(this), viewerurl;
			btn_logs.disable();
			$.ajaxSetup({async: false});
			$.post(
				'/reportes/historial',
				data = {'_xsrf':getCookie('_xsrf'), 'id_per':o_key},
				function(response){
					if(response){
						if(oBrowser && ((oBrowser.app=='Chrome' && oBrowser.ver>=45) || (oBrowser.app=='Opera' && oBrowser.ver>=32))){
							viewerurl = 'data:application/pdf;base64,{0}'.format(response);
						} else{
							var blob = new Blob([$.base64.decode(response)], {type:'application/pdf'}),
								url = URL.createObjectURL(blob);
							viewerurl = 'http://{0}/viewerpdf?file={1}'.format(location.host,encodeURIComponent(url));
						}
					}
				}
			);
			$.ajaxSetup({async: true});
			if(viewerurl && viewerurl.length){
				window.open(viewerurl, strWindowFeatures);
			}
			btn_logs.enable();
		}
	});
	$('#custom, #neo-natos').customPaginator({sort:false,range:[3,5]});
	//$('#neo-natos').customPaginator({height:'auto',range:[3,5]});
});