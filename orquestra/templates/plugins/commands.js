
function activateMenu(menulink) {
	$('#top-menu .item').removeClass('active');
	$('#'+menulink).addClass('active');
}

function orquestra_load_current_view(){
	var href = window.location.href;
	var anchor = href.substring( href.indexOf('#')+1);
	if( anchor.substring(0,5)!='view-' ){ 
		{{ home_function|safe }};
	};
	var paramsStartIndex = anchor.indexOf('|');
	if( paramsStartIndex<0) paramsStartIndex = paramsStartIndex.length;
	var view = anchor.substring(5, paramsStartIndex);
	var params = anchor.substring(paramsStartIndex+1).split('+');

	{% for ifcode in views_ifs %}{{ ifcode|safe }}{% endfor %}	
};

$(orquestra_load_current_view);