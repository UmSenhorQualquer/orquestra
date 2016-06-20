function loading()		{ $("#loading-label").addClass('active'); 		};
function not_loading()	{ $("#loading-label").removeClass('active'); 	};
function show_msgs()	{ 												};
function update_msgs_icon(){ 
	$.get( "/plugins/messages/unread_msg_count/", function(data){
		
		if($('#menu-messages .label').size()>0) $('#menu-messages .label').remove();

		if(data.count>0){
			var html = '<div class="ui label '+data.color+'">'+data.count+'</div>';
			$('#menu-messages').append(html);
		}
	}, "json" );
};


function launch_msgs_check(){
	update_msgs_icon();
	setTimeout(launch_msgs_check, 30000);
}

function success_msg(msg){
	update_msgs_icon();
};

function error_msg(msg){
	update_msgs_icon();
};


function get_current_folder(){
	if($('#MyAreaAppID-_directory').length)
		return $('#MyAreaAppID-_directory').val();
	else
		return '/';
};



var tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close' role='presentation'>Remove Tab</span></li>";

// actual addTab function: adds new tab using the input from the form above
function add_tab(name, label, url) {
	var tabname = "tab-" + name;

	if($('#applications-tab .app-tab.tab[data-tab="'+tabname+'"]').size()==0){

		$('#applications-tab .app-tab.item').removeClass('active');
		$('#applications-tab .app-tab.tab').removeClass('active');

		var html = '<a class="item active app-tab" data-tab="'+tabname+'">'+label+' &nbsp;&nbsp;<i class="power icon"></i></a>';
		$('#applications-tab .apps-tabs').append(html);

		var html = '<div class="ui attached active tab app-tab" id="top-pane" data-tab="'+tabname+'"></div>';
		$('#applications-tab').append(html);

		$('#applications-tab .app-tab.item[data-tab="'+tabname+'"]').on('click', function() {

			$('#applications-tab .item.app-tab').removeClass('active');
			$('#applications-tab .tab.app-tab').removeClass('active');
			$(this).addClass('active');
			$('#applications-tab .tab.app-tab[data-tab="'+$(this).attr('data-tab')+'"]').addClass('active');
		});

		$('#applications-tab .app-tab.item[data-tab="'+tabname+'"] i.power').on('click', function(){

			$('#confirm-tab-close').modal({
				closable  : false,
				onDeny    : function(){return true;},
				onApprove : function() {
					$('#applications-tab .app-tab.tab[data-tab="'+tabname+'"]').remove();
					$('#applications-tab .app-tab.item[data-tab="'+tabname+'"]').prev().click();
					$('#applications-tab .app-tab.item[data-tab="'+tabname+'"]').remove();				  
					return true;
				}
			}).modal('show');

		});
	};

	$('#applications-tab .app-tab.tab[data-tab="'+tabname+'"]').load(url, function(response, status, xhr){
		if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
		not_loading();
	});

	

	
}

function select_main_tab(){
	$('#applications-tab .item[data-tab="tab-home"]').click();
}


var refreshEvent = setInterval(function(){},100000);


function open_application(application){
	add_tab(application, application, "/plugins/applist/load/"+application+"/");
}

$(function(){
	launch_msgs_check();
});