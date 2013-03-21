ngds.SearchResult = function(raw_result) {
	(function() {
		if(raw_result===null || typeof raw_result==='undefined') {
			throw "Expected raw_result to not be null or undefined.";
		}
	})();

	var from_ckanlib;

	if(this.ckanlib!==null && typeof this.ckanlib !== 'undefined') {
		from_ckanlib=function(params) {
			var response_container = function(response) {
				return response;
			};

			var func_dict = {
				'author':this.ckanlib.get_responsible_party,
				'maintainer':this.ckanlib.get_responsible_party
			};

			return func_dict[params['type']](params['id'],response_container);
		}		
	}
	else {
		from_ckanlib=function(param,key) {
			return null;
		}
	}

	var func_map = {
		'count':raw_result.count,
		'author_email':raw_result.author_email,
		'id':raw_result.id,
		'maintainer':from_ckanlib
	}

	return {
		get:function(key,params) {
			if(params === null) {
				return func_map[key]
			}
			return func_map[key](params)
		}
	};
};

(function(ckanlib) {
	ngds.SearchResult.ckanlib = ckanlib;
})(ngds.ckanlib);