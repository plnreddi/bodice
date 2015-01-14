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

	/*	
	pdfMake.createPdf({ content: 'This is an sample PDF printed with pdfMake' }).open();
	$http.get('api/basicbodice').
  */
  
  var user_data = [  37.5,   22.0,  105.0,  40.0,  90.0,  20.0, 
                    117.5,  100.0,  125.0,  12.5,  32.5,  35.0, 
                     22.5,   28.5,   15.0,  14.0  ]
  $scope.form = {};

  $scope.form.keys = ['NeckCirc',   'ArmScyeDepth', 'BustCirc',     'Nape2Waist', 'WaistCirc',  'Waist2Hip',  
                'HipCirc',    'DressLength',  'BottomCirc',   'Shoulder',   'ChestWidth', 'BackWidth', 
                'BreastDist', 'BustHeight',   'SleeveLength', 'SleeveCirc' ]
        
   $scope.form.desc = ['Neck Circumference', 'ArmScye Depth', 'Bust Circumference',   'Nape to Waist', 'Waist Circumference', 'Waist to Hip',  
                'Hip Circumference',  'Dress Length',  'Bottom Circumference', 'Shoulder',      'Chest Width',         'Back Width',
                 'Breast Distance',   'Bust Height',   'Sleeve Length',        'Sleeve Circumference'  ]


  $http.post('api/basicbodice', {usr_data: user_data}).   
  //$http.get('api/basicbodice').
	    success(function(data, status, headers, config) {
	        $scope.basicbodice = data;

          var pts = $scope.basicbodice['data']
          var shp = []
          for(var i=0; i<pts.length; i++){
          	shp[i] = 'M' + pts[i].join(" L");
          }
          $scope.shape = shp;
	    }).

	    error(function(data, status, headers, config) {
	      // log error

	    });
	    
  });
