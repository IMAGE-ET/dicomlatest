angular.module('dicomApp', ['ngResource'])
	.filter('filename', function(){
		return function(input) {
			var out = input.split("/")[2];
			out = out.split(".")[0];
			return out;
		};
	})
	.factory('DicomDetail', ['$resource', function($resource){
		return $resource('/api/documentdetails/:docid', {});
	}])
	.controller('DicomDetailController', ['$scope', 'DicomDetail', function($scope, DicomDetail){
		//$scope.dicom = DicomDetail.get(docid=docid);
		$scope.gup = function (name) {
		  var url = location.href
		  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
		  var regexS = "[\\?&]"+name+"=([^&#]*)";
		  var regex = new RegExp( regexS );
		  var results = regex.exec( url );
		  return results == null ? null : results[1];
		};
		var doc_id = $scope.gup('doc_id');
		$scope.dicom = DicomDetail.get({doc_id});
	}]);