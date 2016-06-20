var RowSorting = (function(){
	
	var column = 0;
	var sortAscending = { 
		sortAlphaAnchor: true,
		sortAlpha: true,
		sortDate: true
	};


	var resetSorting = function(exceptID) {
		if(0 != exceptID) RowSorting.sortAscending.sortAlphaAnchor = true;
		if(1 != exceptID) RowSorting.sortAscending.sortAlpha = true;
		if(2 != exceptID) RowSorting.sortAscending.sortDate = true;
	};

	var resetSortingOrder = function () {
		if(0 == RowSorting.column) RowSorting.resetSorting(0);
                if(1 == RowSorting.column) RowSorting.resetSorting(1);
                if(2 == RowSorting.column) RowSorting.resetSorting(2);
	};

	var toggleSortingOrder = function() {
                if(0 == RowSorting.column) RowSorting.sortAscending.sortAlphaAnchor = !RowSorting.sortAscending.sortAlphaAnchor;
                if(1 == RowSorting.column) RowSorting.sortAscending.sortAlpha = !RowSorting.sortAscending.sortAlpha;
                if(2 == RowSorting.column) RowSorting.sortAscending.sortDate = !RowSorting.sortAscending.sortDate;
	};

	var sortAlphaAnchor = function(a, b) {
		var ret = 0;
		if (a.file < b.file) ret = (RowSorting.sortAscending.sortAlphaAnchor) ? -1 : 1;
		if (a.file > b.file) ret = (RowSorting.sortAscending.sortAlphaAnchor) ? 1 : -1;
		return ret;		
	};

	var sortAlpha = function(a, b) {
		var ret = 0;
		if (a.values[RowSorting.column] < b.values[RowSorting.column]) ret = (RowSorting.sortAscending.sortAlpha) ? -1 : 1;
		if (a.values[RowSorting.column] > b.values[RowSorting.column]) ret = (RowSorting.sortAscending.sortAlpha) ? 1 : -1;
		return ret;
	};

	var sortDate = function(a, b) {
		var ret = 0;
		d1 = new Date(a.values[RowSorting.column]);
		d2 = new Date(b.values[RowSorting.column]);
		if (d1 < d2) ret = (RowSorting.sortAscending.sortDate) ? -1 : 1;
		if (d1 > d2) ret = (RowSorting.sortAscending.sortDate) ?  1 : -1;
		return ret;
	};

	var sortPass = function(a, b) {
		return 0;
	}

	return {
		resetSorting: resetSorting,
		resetSortingOrder: resetSortingOrder,
		toggleSortingOrder: toggleSortingOrder,
		sortAscending: sortAscending,
		sortAlphaAnchor: sortAlphaAnchor,
		sortAlpha: sortAlpha,
		sortDate: sortDate,
		sortPass: sortPass
	};

})();