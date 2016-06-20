function removeFile(filename, file_num){
	$.ajax({
		method: 'post',
		cache: false,
		dataType: "json",
		url: '/removefile/',
		data: {'filename': filename},
		success: function(res){
			update_my_files();
		}
	});
}


(function( $ ){
	jQuery.fn.extend( {
		dataviewer: function(options){
			var self = this;
			var settings = this.data('settings_'+self.selector.replace("#",''));
			var firstTime = false;

			if(!settings){ //Not loaded
				settings = {
					path: '/',
					url: '',
					extra_buttons: [],
					searchField: true,
					editable: false,
					thumb_button: true,
					list_button: true,
					showCheckbox: false,
					thumb_column: true,
					show_crumbs: true,
					limit: 30,
					titles: [],
					values: [],
					sizes: [],
					sortingColumns: [],
					view: 'list',
					cellEdited: null,
					updateRowFunction: null,
					topbar: { background_color: "#FFF" },
					dataviewer: { background_color: "#FFF" },
					afterLoad: null, //call after the ajax load is done
					beforeLoad: null //call before the ajax load is done
				}
				jQuery.extend(settings, options || {});

				var view = Cookies.get('dataviewer-data-view'+self.selector.replace("#",'')); 
				if(view) settings.view = view;
				if(settings.url==='') settings.searchField=false;
				this.settings = settings;
				
				this.html("<div class='dataviewer-bar' ></div><div class='dataviewer-data' ></div>");
				if(settings.show_crumbs) this.find(".dataviewer-bar").append("<div class='dataviewer-bar-path' ></div>");
				if(settings.extra_buttons.length>0) this.find(".dataviewer-bar").append("<div class='dataviewer-bar-buttons' ></div>");
				this.find(".dataviewer-bar").css("background-color", settings.topbar.background_color)
				
				if( settings.searchField ){
					this.find(".dataviewer-bar-path").append("<input placeholder='Search' type='text' class='dataviewer-search-field' />");
					this.find(".dataviewer-bar-path .dataviewer-search-field").keypress(function(e){
						var code = e.keyCode || e.which;
						if(code == 13){ 
							settings.limit = 30;
							self.data('settings_'+self.selector.replace("#",''), settings);
							self.refresh();
						}
					});
				}
				
				for(var i=0; i<settings.extra_buttons.length; i++){
					var btnid = settings.extra_buttons[i].btnId;
					var label = settings.extra_buttons[i].btnLabel;
					var action = settings.extra_buttons[i].btnAction;
					this.find(".dataviewer-bar-buttons").append("<div class='dataviewer-bar-icon'><div class='dataviewer-bar-icon-custom' id='"+btnid+"' >"+label+"</div>");
					this.find(".dataviewer-bar-buttons .dataviewer-bar-icon #"+btnid).click(action);
				}
				if( settings.list_button){
					this.find(".dataviewer-bar-buttons").append("<div class='dataviewer-bar-icon'><div class='dataviewer-bar-icon-list' ></div></div>");
					this.find(".dataviewer-bar-buttons .dataviewer-bar-icon .dataviewer-bar-icon-list").click(function(){
						self.dataviewer({view:'list'});
					});
				};
				if( settings.thumb_button){
					this.find(".dataviewer-bar-buttons").append("<div class='dataviewer-bar-icon'><div class='dataviewer-bar-icon-thumb' ></div></div>");   
					this.find(".dataviewer-bar-buttons .dataviewer-bar-icon .dataviewer-bar-icon-thumb").click(function(){
						self.dataviewer({view:'thumb'});
					});
				};
				
				this.find(".dataviewer-bar").css("background-color", settings.topbar.background_color)
				this.find(".dataviewer-data").css("background-color", settings.dataviewer.background_color)

				self.append("<div class='dataviewer-load-more' >Load more</div>");
				self.find(".dataviewer-load-more").click(function(){
					settings.limit += 30;
					self.data('settings_'+self.selector.replace("#",''), settings);
					self.refresh();
				});

				firstTime = true;
			}else{
				jQuery.extend(settings, options || {});
			}
			if( (typeof options)=='string' ) return settings[options];

			this.data('settings_'+self.selector.replace("#",''), settings);
		  
		  	this.getvalues = function(){
		  		var res=[];
		  		$(self).find('.tableviewer-row').each(function(i,row){

		  			var row = ['..'];
		  			$(this).children('td').each(function(j,col){
		  				row.push( $(this).html() );
		  			});
		  			res.push(row);
		  		});
		  		alert(self.html());
		  		return res;
		  	};
		   
			this.selectedrows = function(){
				var rows = Array();
				$('.dataviewer-data-list-checkbox:checked').each(function( index, value ){
					rows.push( $(this).attr('row-id') );
				});
				return rows;
			};

			this.refresh = function(){
				var query = self.find(".dataviewer-bar-path .dataviewer-search-field").val();
				var sortby = Array();

				$(self).find(".dataviewer-data-list-title .sortUp, .dataviewer-data-list-title .sortDown").each(function(i,e){
					var index = $(this).attr('colindex');
					if( $(this).hasClass('sortUp') ){
						sortby.push('-'+index);
					}
					if( $(this).hasClass('sortDown') ){
						sortby.push(index);
					}
				});

				self.data('selectedRows', self.selectedrows());
				
				if(settings.url){
					if(settings.beforeLoad){ settings.beforeLoad();}
					$.ajax({
						dataType: "json",
						url: settings.url,
						data: {'q':query, 's': sortby.join(','), n:settings.limit },
						success: function(res){
							$(self).dataviewer({values:res});
						},
						error: function(xhr){
							error(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
						}
					}).always(function(){
						if(settings.afterLoad) settings.afterLoad();
					});
				};
			};

			if(!options){
				this.refresh();
			}else{
				if(firstTime) self.refresh();

				if(settings.path){
					self.find(".dataviewer-bar-path .path").remove();
					self.find(".dataviewer-bar-path").append('<span class="path" ></span>');
					var folders = settings.path.split('/');
					var total = folders.length;
					$(folders).each(function(i, e){
						if (i===total-1)
							self.find(".dataviewer-bar-path .path").append(e);
						else
							self.find(".dataviewer-bar-path .path").append(e+"<div class='dataviewer-bar-path-folder-separator'></div>");
					});
				}
				if(settings.values){
					Cookies.set('dataviewer-data-view'+this.selector.replace("#",''), settings.view);

					if(settings.view=='list'){

						//If the table doesn't exists create it
						if( self.find(".dataviewer-data .dataviewer-data-list").length<=0){

							self.find(".dataviewer-data").html("<table class='dataviewer-data-list' ></table>");
						
							//Init titles row
							if( settings.titles.length ){
								var titles = "<tr>";
								if(settings.thumb_column) titles += '<td></td>';

								$(settings.titles).each(function(i, e){
									//Set the size of each column
									var style='';
									if(i<settings.sizes.length) style='style="width:'+settings.sizes[i]+'"';
									titles += "<td "+style+" class='dataviewer-data-list-title' >"+e+" <span colindex='"+i+"' >&nbsp;&nbsp;&nbsp;</span></td>";
								});
								if(settings.showCheckbox){
									titles += "<td></td>";
								}
								titles += "</tr>";

								self.find(".dataviewer-data-list").append(titles);
								
								self.find(".dataviewer-data-list-title").unbind('click');
								self.find(".dataviewer-data-list-title").click(function(){
									var index = $(this).find('span').attr('colindex');
									
									if( $.inArray(parseInt(index), settings.sortingColumns)<0 ) return; //Check if the column should be sorted

									if( $(this).find('span').hasClass('sortDown') ){
										$(this).find('span').removeClass('sortDown');
										$(this).find('span').addClass('sortUp');
									}else if( $(this).find('span').hasClass('sortUp') ){
										$(this).find('span').removeClass('sortUp');
									}else{
										$(this).find('span').addClass('sortDown');
									}
									self.refresh();
								});
							}
						}else{
							self.find(".dataviewer-data .dataviewer-data-list tr").not(':first').remove();
						}

						self.find('.dataviewer-load-more').hide();
						$(settings.values).each(function(i, e){
							if(settings.updateRowFunction)  e = settings.updateRowFunction(e, self);


							self.find(".dataviewer-data-list").append("<tr row-id='"+e.id+"' class='tableviewer-row' id='dataviewer-data-list-row"+i+"' ></tr>");
							if(e=='more')
								self.find('.dataviewer-load-more').show();
							else{
								

								if(settings.thumb_column){
									if(e.small_thumb){
										self.find("#dataviewer-data-list-row"+i).append("<td class='small-thumb' ><img src='"+e.small_thumb+"' /></td>");
									}else{
										self.find("#dataviewer-data-list-row"+i).append("<td class='small-thumb' ></td>");
									}
								}

								$(e.values).each(function(j,el){
									self.find("#dataviewer-data-list-row"+i).append("<td id='dataviewer-data-list-row"+i+"-col"+j+"' >"+el+"</td>");
								});
								if(e.values.length<settings.titles.length){
									for(var j=e.values.length; j<settings.titles.length; j++)
										self.find("#dataviewer-data-list-row"+i).append("<td id='dataviewer-data-list-row"+i+"-col"+j+"' ></td>");
								}



								if(settings.showCheckbox){
									var selectedRows = self.data('selectedRows');
									if(selectedRows==undefined) selectedRows = Array();
									var checked = '';
									if( selectedRows.indexOf(""+e.id)>=0 ) checked="checked='checked'"
									self.find("#dataviewer-data-list-row"+i).append("<td style='width:16px;' ><input class='dataviewer-data-list-checkbox' row-id='"+e.id+"' type='checkbox' "+checked+" /></td>");
								}
							}
						});

						if(settings.editable){
							self.find(".tableviewer-row td").dblclick(function(){
								var cell = $(this);
								var value = cell.html();
								cell.html('<input type="text" value="'+value+'" />');
								cell.children('input').focus();
								cell.children('input').focusout(function(){
									cell.html($(this).val());
									if(settings.cellEdited) settings.cellEdited();
								});
							});
						}
					}
					if(settings.view=='thumb'){
						self.find(".dataviewer-data").html("");
						$(settings.values).each(function(i, e){
							self.find(".dataviewer-data").append("<div class='dataviewer-data-thumb' id='dataviewer-data-thumb"+i+"' ><img src='"+e.big_thumb+"' />"+e.values[0]+"</div>");
						});
					}

				}
			}
		return this;
		}
	})
})( jQuery )




$(function(){
	$('#files-browser-div').dataviewer({ titles:['Filename', 'Size', 'Date',''] });
});