ngds.CKANDataset = function(raw) { // Exposes a set of functions and objects to work with datasets obtained from ckan.

	var me = this;
	this.dataset = raw;

	(function(raw) {
		if(raw===null || typeof raw==='undefined') {
			throw "Passed in object was null or undefined.";
		}
	})(raw);

	_ckan_dataset = {
		construct:function() {
			var spatial_extra;
			$.each(raw.extras,function(index,val) {
				console.log(raw);
				if(val.key==='spatial')	{
					spatial_extra = val.value;
				}
			});
			console.log(spatial_extra);
			var geojson = $.parseJSON(spatial_extra);
			console.log(geojson);
			var description = raw.notes;
			var popupHTML = '<p>';
			popupHTML+='<b> Title : '+raw.title+'</b><br>';
			popupHTML+='Author : '+raw.author+'<br>';
			popupHTML+='Description : '+description+'<br>';
			popupHTML+='Published : '+(new Date()).toLocaleDateString()+'<br>';
			popupHTML+='</p>';

			return {
						getGeoJSON:function() { // return the geojson feature associated with the dataset.
							return geojson;
						},
						map:{
							getPopupHTML:function() { // return a html popup of a dataset's metadata that is to be displayed when an icon or feature is clicked.
								return popupHTML;
								}
							}
			}
		}
	}
	return _ckan_dataset.construct();
};
