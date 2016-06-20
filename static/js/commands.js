function runApplistLoadjob(application,job){
	loading();
	activateMenu('menu-applist');
add_tab("LoadJob", "Reload job", "/plugins/applist/loadjob/"+application+"/"+job+"/");}

function runApplistLoad(application){
	loading();
	activateMenu('menu-applist');
	open_application(application);
}

function runApplist(){
	loading();
	activateMenu('menu-applist');
	clearInterval(refreshEvent);

						select_main_tab();
						$('#top-pane').load("/plugins/applist/applist/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runJobslist(){
	loading();
	activateMenu('menu-jobslist');
	clearInterval(refreshEvent);

						select_main_tab();
						$('#top-pane').load("/plugins/jobslist/jobslist/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runMyclusters(){
	loading();
	activateMenu('menu-myclusters');
	clearInterval(refreshEvent);

						select_main_tab();
						$('#top-pane').load("/plugins/myclusters/myclusters/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runMyserversBrowseservers(){
	loading();
	activateMenu('menu-myservers');
}

function runMyservers(){
	loading();
	activateMenu('menu-myservers');
	clearInterval(refreshEvent);

						select_main_tab();
						$('#top-pane').load("/plugins/myservers/myservers/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runMyserversStart(server_id){
	loading();
	activateMenu('menu-myservers');
}

function runMyserversStop(server_id){
	loading();
	activateMenu('menu-myservers');
}

function runMyareaUpload_delete(){
	loading();
	activateMenu('menu-myarea');
}

function runMyareaUpload(){
	loading();
	activateMenu('menu-myarea');
}

function runMyarea(){
	loading();
	activateMenu('menu-myarea');
	clearInterval(refreshEvent);

						select_main_tab();
						$('#top-pane').load("/plugins/myarea/myarea/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runMyareaUpload_form(){
	loading();
	activateMenu('menu-myarea');
}

function runMyareaBrowse(){
	loading();
	activateMenu('menu-myarea');
}

function runMessages(){
	loading();
	activateMenu('menu-messages');
	clearInterval(refreshEvent);

						select_main_tab();
						$('#top-pane').load("/plugins/messages/messages/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runMessagesUnread_msg_count(){
	loading();
	activateMenu('menu-messages');
}

function runAdminstats(){
	loading();
	activateMenu('menu-adminstats');
	clearInterval(refreshEvent);

						select_main_tab();
						$('#top-pane').load("/plugins/adminstats/adminstats/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runMysettings(){
	loading();
	activateMenu('menu-mysettings');
	clearInterval(refreshEvent);

						select_main_tab();
						$('#top-pane').load("/plugins/mysettings/mysettings/", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});
}

function runAdminarea(){
	loading();
	activateMenu('menu-adminarea');
window.open('/plugins/adminarea/adminarea/');}



function activateMenu(menulink) {
	$('#top-menu .item').removeClass('active');
	$('#'+menulink).addClass('active');
}

function showBreadcrumbs(breadcrumbs, label){
	var html = '';
	for(var i=0; i<breadcrumbs.length; i++){
		html = "<a href='#view-"+breadcrumbs[i][1]+"' onclick='"+breadcrumbs[i][2]+"' >"+breadcrumbs[i][0]+"</a>"
		html += " > ";
	}
	html += label;
	$('#content-breadcrumbs').html(html);
}

function LoadCurrentView(){
	var href = window.location.href;
	var anchor = href.substring( href.indexOf('#')+1);
	if( anchor.substring(0,5)!='view-' ) return;
	var paramsStartIndex = anchor.indexOf('|');
	if( paramsStartIndex<0) paramsStartIndex = paramsStartIndex.length;
	var view = anchor.substring(5, paramsStartIndex);
	var params = anchor.substring(paramsStartIndex+1).split('+');

	if(view=='applist-loadjob') runApplistLoadjob.apply(null, params);
	if(view=='applist-load') runApplistLoad.apply(null, params);
	if(view=='applist') runApplist.apply(null, params);
	if(view=='jobslist-check_job_output') runJobslistCheck_job_output.apply(null, params);
	if(view=='jobslist-check_job_parameters') runJobslistCheck_job_parameters.apply(null, params);
	if(view=='jobslist') runJobslist.apply(null, params);
	if(view=='jobslist-kill_job') runJobslistKill_job.apply(null, params);
	if(view=='jobslist-check_output_files') runJobslistCheck_output_files.apply(null, params);
	if(view=='jobslist-reset_job') runJobslistReset_job.apply(null, params);
	if(view=='jobslist-run_job') runJobslistRun_job.apply(null, params);
	if(view=='myclusters') runMyclusters.apply(null, params);
	if(view=='myservers-browseservers') runMyserversBrowseservers.apply(null, params);
	if(view=='myservers-synchronize_server') runMyserversSynchronize_server.apply(null, params);
	if(view=='myservers') runMyservers.apply(null, params);
	if(view=='myservers-installcluster') runMyserversInstallcluster.apply(null, params);
	if(view=='myservers-start') runMyserversStart.apply(null, params);
	if(view=='myservers-stop') runMyserversStop.apply(null, params);
	if(view=='myservers-check_new_jobs') runMyserversCheck_new_jobs.apply(null, params);
	if(view=='myarea-upload_delete') runMyareaUpload_delete.apply(null, params);
	if(view=='myarea-upload') runMyareaUpload.apply(null, params);
	if(view=='myarea') runMyarea.apply(null, params);
	if(view=='myarea-upload_form') runMyareaUpload_form.apply(null, params);
	if(view=='myarea-browse') runMyareaBrowse.apply(null, params);
	if(view=='messages') runMessages.apply(null, params);
	if(view=='messages-unread_msg_count') runMessagesUnread_msg_count.apply(null, params);
	if(view=='adminstats') runAdminstats.apply(null, params);
	if(view=='mysettings') runMysettings.apply(null, params);
	if(view=='adminarea') runAdminarea.apply(null, params);
	
}