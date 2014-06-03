get_clients = function($scope, $http) {
	$http.get('/clients/').success(function(data)
    {
        $scope.clients = data.clients;
        $scope.client_name = '';
    })
}

get_vehicle_types = function($scope, $http) {
	$http.get('/vehicle_type/list/').success(function(data){
		$scope.vehicle_types = data.vehicle_types;
	})
}

function AddClientController($scope, $http, $location) {

	$scope.client = {
		'name': '',
		'nationality': '',
		'dob': '',
		'home_ph_no': '',
		'work_ph_no': '',
		'license_no': '',
		'license_type': '',
		'date_of_license_issue': '',
		'issued_by': '',
		'expiry_date': '',
		'passport_no': '',
		'passport_issued_date': '',
		'place_of_issue': '',
	};
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
		new Picker.Date($$('#passport_issued_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#expiry_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#dob'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
            canAlwaysGoUp: ['months', 'years']
        });
        new Picker.Date($$('#date_of_license_issue'), {
        	timePicker: false,
        	positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        })
	}

	$scope.validate_client_form = function() {
		$scope.client.dob = $$('#dob')[0].get('value');
		$scope.client.date_of_license_issue = $$('#date_of_license_issue')[0].get('value');
		$scope.client.expiry_date = $$('#expiry_date')[0].get('value');
		$scope.client.passport_issued_date = $$('#passport_issued_date')[0].get('value');
		if ($scope.client.name == '' || $scope.client.name == undefined) {
			$scope.validation_error = 'Please enter the name of the client';
			return false;
		} else if ($scope.client.nationality == '' || $scope.client.nationality == undefined) {
			$scope.validation_error = 'Please enter the nationality';
			return false;
		} else if ($scope.client.dob == '' || $scope.client.dob == undefined) {
			$scope.validation_error = 'Please enter the date of birth';
			return false;
		} else if ($scope.home_address == '' || $scope.home_address == undefined) {
			$scope.validation_error = 'Please enter the home address';
			return false;
		} else if ($scope.client.home_ph_no == '' || $scope.client.home_ph_no == undefined) {
			$scope.validation_error = 'Please enter the Tel. no(home)';
			return false;
		} else if ($scope.work_address == '' || $scope.work_address == undefined) {
			$scope.validation_error = 'Please enter work address';
			return false;
		} else if ($scope.client.work_ph_no == '' || $scope.client.work_ph_no == undefined) {
			$scope.validation_error = 'Please enter Tel. no(work)';
			return false;
		} else if ($scope.client.license_no == '' || $scope.client.license_no == undefined) {
			$scope.validation_error = 'Please enter License  no.';
			return false;
		} else if ($scope.client.license_type == '' || $scope.client.license_type == undefined) {
			$scope.validation_error = 'Please choose License Type';
			return false;
		} else if ($scope.client.date_of_license_issue == '' || $scope.client.date_of_license_issue == undefined) {
			$scope.validation_error = 'Please choose Date of license issued';
			return false;
		} else if ($scope.client.issued_by == '' || $scope.client.issued_by == undefined) {
			$scope.validation_error = 'Please enter issued by';
			return false;
		} else if ($scope.client.expiry_date == '' || $scope.client.expiry_date == undefined) {
			$scope.validation_error = 'Please choose expiry date';
			return false;
		} else if ($scope.client.passport_no == '' || $scope.client.passport_no == undefined) {
			$scope.validation_error = 'Please enter Passport no.';
			return false;
		} else if ($scope.client.passport_issued_date == '' || $scope.client.passport_issued_date == undefined) {
			$scope.validation_error = 'Please choose Passport Issued Date';
			return false;
		} else if ($scope.client.place_of_issue == '' || $scope.client.place_of_issue == undefined) {
			$scope.validation_error = 'Please enter the Place of passport issued';
			return false;
		}
		return true;
	}

	$scope.add_client = function() {
		$scope.is_valid = $scope.validate_client_form();  
		console.log($scope.is_valid);
		if ($scope.is_valid) {
			$scope.validation_error = '';
			params = { 
				'client_work_address': $scope.work_address,
				'client_home_address': $scope.home_address,
                'client_details': angular.toJson($scope.client),
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/add_client/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    document.location.href ='/clients/';
                }
            }).error(function(data, status){
                $scope.validation_error = data.message;
            });
		}
	}

}

function AddVehicleController($scope, $http, $location) {

	$scope.vehicle = {
		'vehicle_no': '',
		'plate_no': '',
		'condition': '',
		'vehicle_type': '',
		'color': '',
		'meter_reading': '',
		'insurance_type': '',
		'insurance_value': '',
	}
	$scope.init = function(csrf_token, id) {
		$scope.csrf_token = csrf_token;
		$scope.id = id;
		get_vehicle_types($scope, $http);
	}

	$scope.add_new_type = function() {
		if ($scope.vehicle.vehicle_type == 'other') {
			$scope.popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#new_vehicle_type'
            });
            var height = $(document).height();
            $scope.popup.set_overlay_height(height);
            $scope.popup.show_content();
		}
	}
	$scope.close_popup = function() {
		$scope.popup.hide_popup();
	}
	$scope.save_new_vehicle_type = function() {
		if ($scope.vehicle_type == '' || $scope.vehicle_type == undefined) {
			$scope.message = 'Please enter the vehicle type';
		} else {
			$scope.message = '';
			params = { 
				'vehicle_type': $scope.vehicle_type,
                "csrfmiddlewaretoken" : $scope.csrf_token,
            }
            $http({
                method : 'post',
                url : "/add_vehicle_type/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    get_vehicle_types($scope, $http);
                    $scope.vehicle.vehicle_type = data.vehicle_type_name;
                    $scope.close_popup();
                    // document.location.href ='/clients/';
                }
            }).error(function(data, status){
                $scope.message = data.message;
            });
		}
	}
	$scope.validate_vehicle_form = function() {
		if ($scope.vehicle.vehicle_no == '' || $scope.vehicle.vehicle_no == undefined) {
			$scope.validation_error = 'Please enter Vehicle No.';
			return false;
		} else if ($scope.vehicle.plate_no == '' || $scope.vehicle.plate_no == undefined) {
			$scope.validation_error = 'Please enter Plate No.';
			return false;
		} else if ($scope.vehicle.condition == '' || $scope.vehicle.condition == undefined) {
			$scope.validation_error = 'Please enter Vehicle Condition';
			return false;
		} else if ($scope.vehicle.vehicle_type == '' || $scope.vehicle.vehicle_type == undefined || $scope.vehicle.vehicle_type == 'other') {
			$scope.validation_error = 'Please choose Vehicle Type';
			return false;
		} else if ($scope.vehicle.color == '' || $scope.vehicle.color == undefined) {
			$scope.validation_error = 'Please enter Vehicle Color';
			return false;
		} else if ($scope.vehicle.meter_reading == '' || $scope.vehicle.meter_reading == undefined) {
			$scope.validation_error = 'Please enter Meter Reading';
			return false;
		} else if ($scope.vehicle.insurance_type == '' || $scope.vehicle.insurance_type == undefined) {
			$scope.validation_error = 'Please enter Insurance Type';
			return false;
		} else if ($scope.vehicle.insurance_value == '' || $scope.vehicle.insurance_value == undefined) {
			$scope.validation_error = 'Please enter Insurance Value';
			return false;
		}
		return true;
	}
	$scope.add_vehicle = function() {
		$scope.is_valid = $scope.validate_vehicle_form();
		if ($scope.is_valid) {
			$scope.validation_error = '';
			params = {
				'vehicle_details': angular.toJson($scope.vehicle),
				"csrfmiddlewaretoken" : $scope.csrf_token,
			}
			$http({
                method : 'post',
                url : "/add_vehicle/",
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                
                if (data.result == 'error'){
                    $scope.error_flag=true;
                    $scope.message = data.message;
                } else {
                    $scope.error_flag=false;
                    $scope.message = '';
                    get_vehicle_types($scope, $http);
                    $scope.vehicle.vehicle_type = data.vehicle_type_name;
                    $scope.close_popup();
                    // document.location.href ='/clients/';
                }
            }).error(function(data, status){
                $scope.message = data.message;
            });
		}
	}

}