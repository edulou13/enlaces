/*!
* auhtor: Luis Eduardo Miranda Barja
* (C) 2015 - mbarjaedu13@gmail.com
*/
$(function(){
	$.fn.customPaginator = function(config){
		//console.log(arguments.length);
		var optRange = function(range){
				var options = [[],[]];
				if(arguments.length){
					for (var i = 0; i < range.length; i++) {
						options[0].push(range[i]); options[1].push(range[i]);
					}
					options[0].push(10); options[1].push(10);
					for(var i=25; i<=100; i=i+25){
						options[0].push(i); options[1].push(i);
					}
				} else{
					options[0].push(10); options[1].push(10);
					for(var i=25; i<=100; i=i+25){
						options[0].push(i); options[1].push(i);
					}
				}
				options[0].push(-1); options[1].push('Todo');
				return options;
			},
			cfg = $.extend({'height': 'auto', sort: true, 'processing': true, 'deferRender': true}, config),
			$cfg = {
				//scrollY: 300,
				scrollX: true,
				//sScrollY: (arguments.length && 'height' in config)?config.height:278,
				//sScrollX: 599,
				sScrollY: cfg.height,
				/*pagingType:'simple_numbers',//'full_numbers'*/
				pagingType: 'full_numbers',
				sort: cfg.sort,
				//lengthMenu: arguments.length==0?optRange():optRange(start,stop,step),
				lengthMenu: ('range' in cfg && cfg.range.length)?optRange(cfg.range):optRange(),
				language:{
					//"lengthMenu": "<span>Mostrar </span>_MENU_<span> datos</span>",
					"lengthMenu": "Mostrar _MENU_<span class='itotal'></span>",
					"zeroRecords": "Sin datos disponibles!",
					"info": "Página _PAGE_ de _PAGES_<i class='ttotal hidden'>_TOTAL_</i>",
					"infoEmpty": "Sin datos",
					//"infoFiltered": "(filtrado de _MAX_ total entradas)",
					"infoFiltered": "",
					"search": "",
					"paginate": {
						"first": " ",//primero
						"previous": " ",//anterior
						"next": " ",//siguiente
						"last": " "//ultimo
					}
				}
			};
		return this.each(function(){
			var custom_dt = $(this).dataTable($cfg).closest('[id$="_wrapper"]'), tmp_total = custom_dt.find('.ttotal');
			custom_dt
				.find('.dataTables_filter').find('input').attr({placeholder:'Buscar'})
					.on({
						click:function(e){
							$(this).val('').trigger('keyup');
						}
					}).end().end()
				.find('.itotal').text(tmp_total.text().length>0?' de '+tmp_total.text():'').end();
			//tmp_total.remove();
			hide_tablelinks(custom_dt);
		});
	};
	$.fn.cfilter = function(data_list){
		var o_select = $('<select class="form-control input-sm cfilter"/>'), list_options = ['<option value="-1">Todo</option>'];
		for(var i in data_list){
			var obj = data_list[i], o_op = $('<option/>');
			o_op.attr({'value':obj.val,'selected':(obj.def==true?true:false)}).text(obj.label);
			list_options.push(o_op);
		};
		o_select.html(list_options).addClass('c_select');
		return this.each(function(){
			var custom_dt = $(this).closest('[id$="_wrapper"]');
			custom_dt
				.find('.row:first').find('.col-sm-6').removeClass('col-sm-6').addClass('col-xs-6').eq(0).html(o_select).end().end().end()
				.find('.dataTables_filter').find('input').val(o_select.val()=='-1'?'':o_select.val()).trigger('keyup').end().end();
			var o_total = custom_dt.find('.ttotal').text();
			custom_dt.find('.itotal').text(o_total.length>0?' de '+o_total:'').end()
				.on('change', '.cfilter', function(event){
					var o_str = $(this).val();
					//console.log(event.type, o_str);
					custom_dt.find('.dataTables_filter').find('input').val(o_str=='-1'?'':o_str).trigger('keyup').end().end();
					var tmp_total = custom_dt.find('.ttotal').text();
					custom_dt.find('.itotal').text(tmp_total.length>0?' de '+tmp_total:'').end();
				});
			// o_select.on({
			// 	'change':function(e){
			// 		var o_str = $(this).val();
			// 		//console.log(e.type, o_str);
			// 		custom_dt.find('.dataTables_filter').find('input').val(o_str=='-1'?'':o_str).trigger('keyup').end().end();
			// 		var tmp_total = custom_dt.find('.ttotal').text();
			// 		custom_dt.find('.itotal').text(tmp_total.length>0?' de '+tmp_total:'').end();
			// 	}
			// });
		});
	};
	var hide_tablelinks = function(o_table){
		var tb = o_table.find('.row').eq(1).find('tbody');
		tb
			.on('mouseover, mouseenter', 'a, .link', function(e){
				var anchor = $(this);
				anchor.data('lnk', anchor.attr('href')).removeAttr('href');
			})
			.on('click', 'a, .link', function(e){
				e.preventDefault();
				location.href = $(this).data('lnk');
			});
	};
});