function loading()		{ /*$("#loading-label").addClass('active'); */		};
function not_loading()	{/* $("#loading-label").removeClass('active'); */	};

function activate_tab(name){
	var tabname = "tab-" + name;
	$('.app-tab').removeClass('active');
	$('.app-tab[data-tab="'+tabname+'"]').addClass('active');
	$('.menu a.item').removeClass('active');
	$('.menu a.item[data-tab="'+tabname+'"]').addClass('active');
};

// actual addTab function: adds new tab using the input from the form above
function add_tab(name, label, url) {
	var tabname = "tab-" + name;

	if($('#applications-tab-menu .app-tab.tab[data-tab="'+tabname+'"]').size()==0){
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
				var html = '<div class="html ui basic segment"><div class="ui container">';
				html += '<h2 class="ui right floated header">'+label+'</h2>';
				html += '<div class="ui clearing divider"></div>';
				html += "<form class='ui form' id='app-"+res.app_id+"' >";
				html += res.code;
				html += '</form>';
				html += '</div></div>';
				$('#applications-tab-content .app-tab.tab[data-tab="'+tabname+'"]').html(html);
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	});
}



function select_main_tab(){
	$('#applications-tab-menu .item[data-tab="tab-home"]').click();
}

function run_application(application){
	$.ajax({
		method: 'get',
		cache: false,
		dataType: "json",
		url: '/pyforms/app/register/'+application+'/?nocache='+$.now(),
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' )
				error_msg(res.msg);
			else
				for(var i=0; i<res.length; i++){
					pyforms.open_application(res[i]);
				};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	});
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
				var html = '<div class="html ui basic segment"><div class="ui container">';
				html += '<h2 class="ui right floated header">'+label+'</h2>';
				html += '<div class="ui clearing divider"></div>';
				html += "<form class='ui form' id='app-"+res.app_id+"' >";
				html += res.code;
				html += '</form>';
				html += '</div></div>';
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
function add_segment(name, label, url) {
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
				var html = '<div class="ui raised floated segment" style="margin:20px; min-width:650px;" >';
				html += '<h2 class="ui right floated header">'+label+'</h2>';
				html += '<div class="ui clearing divider"></div>';
				html += "<form class='ui form' id='app-"+res.app_id+"' >";
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

	/*$('html, body').animate({
        scrollTop: e.offset().top
    }, 500);*/
}

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
function show_window(name, label, url) {
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
				var html = '<div class="header">'+label+'</div>';
				html += '<div class="content">';
				html += "<form class='ui form' id='app-"+res.app_id+"' >";
				html += res.code;
				html += '</form>';
				html += '</div>';
				html += '</div>';			
				$('#dialog').html(html);
				$('#dialog').modal('setting', 'observe Changes', true).modal('setting', 'duration', 0).modal('setting', 'onHide', function(e){
					pyforms.remove_app(res.app_id);
				}).modal('show');
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	}).always(function(){
		pyforms.garbage_collector();
	});
}
function activate_window(name, label, url) {$('#dialog').modal('show');}
function close_window() {$('#dialog').modal('hide');}
/*********************************************************/
/*********************************************************/
/*********************************************************/

$(document).ready(function() {
	pyforms.register_layout_place(5, add_tab, activate_tab);
	pyforms.register_layout_place(6, add_segment);
	pyforms.register_layout_place(0, home);
	pyforms.register_layout_place(4, show_window, activate_window, close_window);
});