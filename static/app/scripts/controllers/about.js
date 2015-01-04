'use strict';

/**
 * @ngdoc function
 * @name staticApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the staticApp
 */
angular.module('staticApp')
  .controller('AboutCtrl', function ($scope, $http) {

	$http.get('api/basicbodice').
	    success(function(data, status, headers, config) {
	      $scope.basicbodice = data;

          var pts = $scope.basicbodice['data']
          var str = pts[1].join(" L");
          $scope.ptstr = 'M' + str


	    }).
	    error(function(data, status, headers, config) {
	      // log error
	    });
	    /*
        var pts = $scope.basicbodice['data']
        $scope.ptstr = pts[0].join("L");
		*/


  });
