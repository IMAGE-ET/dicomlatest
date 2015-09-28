angular.module('dicomApp', ['ngResource'])
	.filter('filename', function(){
		return function(input) {
			var out = input.split("/")[2];
			out = out.split(".")[0];
			return out;
		};
	})
	.factory('Dicom', ['$resource', function($resource){
		return $resource('/api/upload_form_serializer/', {}, {
			get:{method:'GET', isArray:true}
		});
	}])
	.factory('PropKeys', ['$resource', function($resource) {
		return $resource('/api/propkeylist/');
	}])
	.controller('DicomController', ['$scope', 'Dicom', 'PropKeys', function($scope, Dicom, PropKeys){
		$scope.dicoms = Dicom.query();
		if($scope.propkeys === undefined)
			$scope.propkeys = PropKeys.query();
		$scope.querykey = null;
		$scope.queryvalue = null;
		$scope.search = function() {
			$scope.dicoms = Dicom.get({prop_key: $scope.querykey, prop_value:$scope.queryvalue, which:'prop'});
		};
	}]);