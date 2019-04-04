function loading()		{ /*$("#loading-label").addClass('active'); */		};
function not_loading()	{/* $("#loading-label").removeClass('active'); */	};

function activate_tab(name){
	var tabname = "tab-" + name;
	$('.app-tab').removeClass('active');
	$('.app-tab[data-tab="'+tabname+'"]').addClass('active');
	$('.menu a.item').removeClass('active');
	$('.menu a.item[data-tab="'+tabname+'"]').addClass('active');
};


function close_tab(app_id){
	var tabname = "tab-" + app_id;
	$('#applications-tab-content .app-tab.tab[data-tab="'+tabname+'"]').remove();
	$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"]').prev().click();
	$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"]').remove();
};

// actual addTab function: adds new tab using the input from the form above
function add_tab(name, label, url) {
	var tabname = "tab-" + name;

	if($('#applications-tab-menu .app-tab.tab[data-tab="'+tabname+'"]').length==0){
		//begin menu
		$('#applications-tab-menu .app-tab.item').removeClass('active');
		$('#applications-tab-content .app-tab.tab').removeClass('active');

		if(label.length>30) label = label.substring(0,27)+'...';
		var html = '<a class="item active app-tab" data-tab="'+tabname+'">'+label+' &nbsp;&nbsp;<i class="remove icon"></i></a>';
		$('#applications-tab-menu').append(html);

		var html = '<div class="ui attached active tab app-tab container" data-tab="'+tabname+'"></div>';
		$('#applications-tab-content').append(html);

		$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"]').on('click', function() {
			$('#applications-tab-menu .item.app-tab').removeClass('active');
			$('#applications-tab-content .tab.app-tab').removeClass('active');
			$(this).addClass('active');
			$('#applications-tab-content .tab.app-tab[data-tab="'+$(this).attr('data-tab')+'"]').addClass('active');
		});

		$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"] i.remove').on('click', function(){
			$('#confirm-tab-close').modal({
				closable  : false,
				onDeny    : function(){return true;},
				onApprove : function() {
					$('#applications-tab-content .app-tab.tab[data-tab="'+tabname+'"]').remove();
					$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"]').prev().click();
					$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"]').remove();
					pyforms.garbage_collector();				  
					return true;
				}
			}).modal('show');
		});
	};

	$.ajax({
		method: 'get',
		cache: false,
		dataType: "json",
		url: url,
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' )
				error_msg(res.msg);
			else{
				var html = '';
				html += '<div class="app-segment" >'
				html += '<h2 class="ui medium right aligned header app-header">'+label+'</h2>';
				html += "<form onsubmit='return false;' class='ui form "+res.css+"' id='app-"+res.app_id+"' >";
				html += res.code;
				html += '</form>';
				html += '</div>';
				$('#applications-tab-content .app-tab.tab[data-tab="'+tabname+'"]').html(html);
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	});
};


// actual addTab function: adds new tab using the input from the form above
function add_tab_full(name, label, url) {
	var tabname = "tab-" + name;

	if($('#applications-tab-menu .app-tab.tab[data-tab="'+tabname+'"]').length==0){
		//begin menu
		$('#applications-tab-menu .app-tab.item').removeClass('active');
		$('#applications-tab-content .app-tab.tab').removeClass('active');

		if(label.length>30) label = label.substring(0,27)+'...';
		var html = '<a class="item active app-tab" data-tab="'+tabname+'">'+label+' &nbsp;&nbsp;<i class="remove icon"></i></a>';
		$('#applications-tab-menu').append(html);

		var html = '<div class="ui attached active tab app-tab" data-tab="'+tabname+'"></div>';
		$('#applications-tab-content').append(html);

		$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"]').on('click', function() {
			$('#applications-tab-menu .item.app-tab').removeClass('active');
			$('#applications-tab-content .tab.app-tab').removeClass('active');
			$(this).addClass('active');
			$('#applications-tab-content .tab.app-tab[data-tab="'+$(this).attr('data-tab')+'"]').addClass('active');
		});

		$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"] i.remove').on('click', function(){
			$('#confirm-tab-close').modal({
				closable  : false,
				onDeny    : function(){return true;},
				onApprove : function() {
					$('#applications-tab-content .app-tab.tab[data-tab="'+tabname+'"]').remove();
					$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"]').prev().click();
					$('#applications-tab-menu .app-tab.item[data-tab="'+tabname+'"]').remove();
					pyforms.garbage_collector();				  
					return true;
				}
			}).modal('show');
		});
	};

	$.ajax({
		method: 'get',
		cache: false,
		dataType: "json",
		url: url,
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' )
				error_msg(res.msg);
			else{
				var html = '';
				html += '<div class="app-segment" >'
				html += '<h2 class="ui medium right aligned header app-header">'+label+'</h2>';
				html += "<form onsubmit='return false;' class='ui form "+res.css+"' id='app-"+res.app_id+"' >";
				html += res.code;
				html += '</form>';
				html += '</div>';
				$('#applications-tab-content .app-tab.tab[data-tab="'+tabname+'"]').html(html);
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	});
};

function select_main_tab(){
	$('#applications-tab-menu .item[data-tab="tab-home"]').click();
};

function home(name, label, url){
	$.ajax({
		method: 	'get',
		cache: 		false,
		dataType: 	"json",
		url: url,
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' )
				error_msg(res.msg);
			else{
				var html = '';
				html += '<div class="app-segment ui container" >'
				html += '<h2 class="ui medium right aligned header app-header">'+label+'</h2>';
				html += "<form onsubmit='return false;' class='ui form "+res.css+"' id='app-"+res.app_id+"' >";
				html += res.code;
				html += '</form>';
				html += '</div>';
				$('#tab-home').html(html);
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	}).always(function(){
		pyforms.garbage_collector();
	});
};

function home_full(name, label, url){
	$.ajax({
		method: 	'get',
		cache: 		false,
		dataType: 	"json",
		url: url,
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' )
				error_msg(res.msg);
			else{
				var html = '';
				html += '<div class="app-segment ui" >'
				html += '<h2 class="ui medium right aligned header app-header">'+label+'</h2>';
				html += "<form onsubmit='return false;' class='ui form "+res.css+"' id='app-"+res.app_id+"' >";
				html += res.code;
				html += '</form>';
				html += '</div>';
				$('#tab-home').html(html);
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	}).always(function(){
		pyforms.garbage_collector();
	});
};

// actual addTab function: adds new tab using the input from the form above
function append_home(name, label, url) {
	$.ajax({
		method: 	'get',
		cache: 		false,
		dataType: 	"json",
		url: url,
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' )
				error_msg(res.msg);
			else{
				var html = '';
				html += '<div class="ui raised floated segment" style="margin:20px; min-width:650px;" >';
				html += '<h2 class="ui right floated header">'+label+'</h2>';
				html += '<div class="ui clearing divider"></div>';
				html += "<form onsubmit='return false;' class='ui form "+res.css+"' id='app-"+res.app_id+"' >";
				html += res.code;
				html += '</form>';
				html += '</div>';
				$(html).appendTo('#tab-home').show('fadeIn');
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	}).always(function(){
		pyforms.garbage_collector();
	});
};

var refreshEvent = setInterval(function(){},100000);
var msg_timeout = undefined;

function success_msg(msg){
	if(msg_timeout!=undefined) clearTimeout(msg_timeout);
	$('#top-menu').popup({title: 'Success', variation:'basic', on:'manual', content: msg, position:'top center'}).popup('show');
	msg_timeout = setTimeout(function(){$('#top-menu').popup('destroy');}, 5000);
};

function error_msg(msg){
	if(msg_timeout!=undefined) clearTimeout(msg_timeout);
	$('#top-menu').popup({title: 'Error', variation:'basic', on:'manual', content: msg, position:'top center'}).popup('show');
	msg_timeout = setTimeout(function(){$('#top-menu').popup('destroy');}, 10000);
};

function get_current_folder(){
	if($('#MyAreaAppID-_directory').length)
		return $('#MyAreaAppID-_directory').val();
	else
		return '/';
};

/*********************************************************/
/*********************************************************/
/*********************************************************/
function show_window(name, label, url, bigwindow) {
	var dialog_id = "dialog-"+name;

	$.ajax({
		method: 	'get',
		cache: 		false,
		dataType: 	"json",
		url: url,
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' )
				error_msg(res.msg);
			else{
				var window_exists = $('#'+dialog_id).length>0;
				var extra_css = '';
				if(bigwindow)
					var extra_css = 'large';
				if( !window_exists )
					$('body').append(`<div class='ui ${extra_css} modal' id='${dialog_id}' ></div>`);

				var html = '<i class="close icon"></i><div class="header">'+label+'</div>';
					html += '<div class="content">';
					html += "<form onsubmit='return false;' class='ui form"+res.css+"' id='app-"+res.app_id+"' >";
					html += res.code;
					html += '</form>';
					html += '</div>';

				$('#'+dialog_id).html(html);
				
				if( !window_exists )	
					$('#'+dialog_id).modal(
						'setting', 'autofocus', false).modal(
						'setting', 'observe Changes', true).modal(
						'setting', 'duration', 0).modal(
						'setting', 'onHide', function(e){
						pyforms.remove_app(res.app_id);
					}).modal('show');
				else
					$('#'+dialog_id).modal('refresh').modal('show');

				setTimeout(`$('#${dialog_id}').modal('refresh');`, 200);
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	}).always(function(){
		pyforms.garbage_collector();
	});
};
function activate_window(name, label, url) {
	var dialog_id = "dialog-"+name;
	$('#'+dialog_id).modal('show');
};
function close_window(app_id){
	var dialog_id = "dialog-"+app_id;
	$('#'+dialog_id).modal('hide');
	$('#'+dialog_id).remove();
};

function show_bigwindow(name, label, url) {
	show_window(name, label, url, true);
}
/*********************************************************/
/*********************************************************/
/*********************************************************/

$(document).ready(function() {
	pyforms.register_layout_place(0, home);
	pyforms.register_layout_place(1, add_tab, activate_tab, close_tab);
	pyforms.register_layout_place(2, show_window, activate_window, close_window);
	pyforms.register_layout_place(3, append_home);

	pyforms.register_layout_place(4, home_full);
	pyforms.register_layout_place(5, add_tab_full, activate_tab, close_tab);

	pyforms.register_layout_place(6, show_bigwindow, activate_window, close_window);

	pyforms_checkhash_wrapper();
});





