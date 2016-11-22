  function loading()		{ $("#loading-label").addClass('active'); 		};
function not_loading()	{ $("#loading-label").removeClass('active'); 	};

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

function run_application(application){
	$.ajax({
		method: 'get',
		cache: false,
		dataType: "json",
		url: '/plugins/applist/load/'+application+'/?nocache='+$.now(),
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
					}else
						open_application(res[i]);
				};
		}
	}).fail(function(xhr){
		error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	});

};

function open_application(app_data){
	var layout_position = app_data['layout_position'];
	var application_id  = app_data['uid'];
	if(layout_position===5){
		add_tab(application_id, app_data['title'], "/plugins/applist/openapp/"+application_id+"/");
	}else
	if(layout_position===0){
		$('#top-pane').load("/plugins/applist/openapp/"+application_id+"/", function(response, status, xhr){
			if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
			not_loading();
		});
	};
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
	
$(function(){
	BaseWidget.prototype.schedule_job = function(){
		var html= '<table class="ui celled compact table" >';
		
		var currentfolder = get_current_folder();
		if(currentfolder==undefined) currentfolder = '/';

		html += "<thead><tr><th>Field</th><th>Value</th></tr></thead>"
		html += "<tbody>";
		html += "<tr>";
		html += "<td >Output folder</td>";
		html += "<td >"+currentfolder+"<input type='hidden' value='"+currentfolder+"' id='"+this.widget_id+"-job-output-folder' /></td>";
		html += "</tr>";
		for (var index = 0; index < this.controls.length; index++) {
			var name  = this.controls[index].name;
			var value = this.controls[index].get_value();
			var label = this.controls[index].properties.label;

			if((typeof value !== "undefined") && (typeof name !== "undefined") && (typeof label !== "undefined")){
				html+="<tr>";
				html+="<td class='collapsing'>"+label+"</td>";
				html+="<td >"+value+"</td>";
				html+="</tr>";
			}
		}
		html += "</tbody>";
		html += "</table>";
		$('#'+this.widget_id+'-schedulejob-window-content').html( html );

		var self = this;
		$.ajax({
			dataType: "json",
			cache: false,
			url: '/plugins/applist/browseappservers/'+this.name+'/',
			success: function(res){
				var select = document.getElementById(self.widget_id+'-schedulejob-server');
				select.options.length = 0;
				var option=document.createElement("option");
				option.text='Auto'; option.id = 0; select.add(option);

				for (index = 0; index < res.length; index++) {
					var id = res[index][0];
					var name = res[index][1];
					var option=document.createElement("option");
					option.text=name;
					option.id = id;
					select.add(option);
				}
			}
		});
		$('#'+this.widget_id+'-schedulejob-window').modal('show');

	}


	BaseWidget.prototype.send_job_2_queue = function(){
		
		var params = { userpath: $('#'+this.widget_id+'-job-output-folder').val() };
		
		for (var index = 0; index <this.controls.length; index++) {
			var name 	 = this.controls[index].name;
			params[name] = this.controls[index].serialize();			
		}

		var jsondata =  $.toJSON( params );
		var server = $("#"+this.widget_id+"-schedulejob-server").find('option:selected').attr('id');
		$.ajax({
			method: 'post',
			cache: false,
			dataType: "json",
			url: '/plugins/applist/queue/'+this.name+'/'+server+'/',
			contentType: "application/json; charset=utf-8",
			data: jsondata,
			success: function(res){
				success_msg(res.msg);
			},
			error: function(xhr){
				error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
			}
		});
		$('#'+this.widget_id+'-schedulejob-window').modal('hide');
	}

	BaseWidget.prototype.batch_file = function(){
		$('#dialog-window').modal('show');
		$('#dialog-window').load('/load/'+this.application+'/batchfile/');
	}

});