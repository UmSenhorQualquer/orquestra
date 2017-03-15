function loading()		{ /*$("#loading-label").addClass('active'); */		};
function not_loading()	{/* $("#loading-label").removeClass('active'); */	};

// actual addTab function: adds new tab using the input from the form above
function add_tab(name, label, url) {
	var tabname = "tab-" + name;

	if($('#applications-tab .app-tab.tab[data-tab="'+tabname+'"]').size()==0){
		$('#applications-tab .app-tab.item').removeClass('active');
		$('#applications-tab .app-tab.tab').removeClass('active');

		var html = '<a class="item active app-tab" data-tab="'+tabname+'">'+label+' &nbsp;&nbsp;<i class="remove icon"></i></a>';
		$('#applications-tab .apps-tabs').append(html);

		var html = '<div class="ui attached active tab app-tab" id="top-pane" data-tab="'+tabname+'"></div>';
		$('#applications-tab').append(html);

		$('#applications-tab .app-tab.item[data-tab="'+tabname+'"]').on('click', function() {
			$('#applications-tab .item.app-tab').removeClass('active');
			$('#applications-tab .tab.app-tab').removeClass('active');
			$(this).addClass('active');
			$('#applications-tab .tab.app-tab[data-tab="'+$(this).attr('data-tab')+'"]').addClass('active');
		});

		$('#applications-tab .app-tab.item[data-tab="'+tabname+'"] i.remove').on('click', function(){
			$('#confirm-tab-close').modal({
				closable  : false,
				onDeny    : function(){return true;},
				onApprove : function() {
					$('#applications-tab .app-tab.tab[data-tab="'+tabname+'"]').remove();
					$('#applications-tab .app-tab.item[data-tab="'+tabname+'"]').prev().click();
					$('#applications-tab .app-tab.item[data-tab="'+tabname+'"]').remove();
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
				$('#applications-tab .app-tab.tab[data-tab="'+tabname+'"]').html(html);
			};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	});
	
}

// actual addTab function: adds new tab using the input from the form above
function add_segment(name, label, url) {
	var e = $('<div class="ui raised floated segment" style="margin:20px; min-width:800px; display:None;" ></div>').appendTo('#top-pane').load(url, function(response, status, xhr){
		if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	}).transition('scale')

	$('html, body').animate({
        scrollTop: e.offset().top
    }, 500);
}

function select_main_tab(){
	$('#applications-tab .item[data-tab="tab-home"]').click();
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
					var app = pyforms.find_app(res[i]['uid']);
					if( app!=undefined){
						//pyforms.remove_app(res[i]['uid']);
						//run_application(application);
						not_loading();
					}else
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
				$('#top-pane').html(html);
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

$(document).ready(function() {
	pyforms.register_layout_place(5, add_tab);
	pyforms.register_layout_place(0, home);
});