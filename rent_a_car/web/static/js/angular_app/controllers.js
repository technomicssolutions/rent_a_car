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

get_vehicles = function($scope, $http) {
	$http.get('/vehicles/').success(function(data){
		$scope.vehicles = data.vehicles;
	})
}

save_vehicle_type = function($scope, $http, from) {
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
                if (from == 'add_vehicle') {
                	$('#new_vehicle_type').hide();
                	$('#new_vehicle').show();
                } else {
                	$scope.close_popup();
                }
                // document.location.href ='/clients/';
            }
        }).error(function(data, status){
            $scope.message = data.message;
        });
	}
}

validate_vehicle_form = function($scope, $http) {
	if ($scope.vehicle.vehicle_no == '' || $scope.vehicle.vehicle_no == undefined) {
		$scope.validation_error = 'Please enter Vehicle No.';
		return false;
	} else if ($scope.vehicle.plate_no == '' || $scope.vehicle.plate_no == undefined) {
		$scope.validation_error = 'Please enter Plate No.';
		return false;
	} else if ($scope.vehicle.condition == '' || $scope.vehicle.condition == undefined) {
		$scope.validation_error = 'Please enter Vehicle Condition';
		return false;
	} else if ($scope.vehicle.vehicle_make == '' || $scope.vehicle.vehicle_make == undefined) {
		$scope.validation_error = 'Please enter Vehicle Make';
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
add_vehicle = function($scope, $http, from) {
	$scope.is_valid = validate_vehicle_form($scope, $http);
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
            if (from != 'add_vehicle') {
            	document.location.href ='/vehicles/';
            } else {
            	$scope.vehicle_data = data.vehicle_data[0];
            	get_vehicles($scope, $http);
            	$scope.vehicle = data.vehicle_data[0];
            	$scope.close_popup_add_vehicle();
            }
        }).error(function(data, status){
            $scope.validation_error = data.message;
        });
	}
}
validate_client_form = function($scope, $http) {
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

add_client = function($scope, $http, from) {
	$scope.is_valid = validate_client_form($scope, $http);  
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
                if(from != 'client_popup') {
                	document.location.href ='/clients/';
                } else {
                	$scope.client_data = data.client_data[0];
	            	get_clients($scope, $http);
	            	$scope.client = data.client_data[0];
	            	$scope.close_popup_add_client();
                }
                	
            }
        }).error(function(data, status){
            $scope.validation_error = data.message;
        });
	}
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
		'vehicle_make': '',
	}
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
		get_vehicle_types($scope, $http);
	}

	$scope.add_new_type = function() {
		$scope.message = '';
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
		save_vehicle_type($scope, $http, '');
	}
	$scope.add_vehicle = function() {
		$scope.is_valid = validate_vehicle_form($scope, $http);
		if ($scope.is_valid) {
			add_vehicle($scope, $http, '');
		}
	}

}

function EditVehicleController($scope, $http, $location) {

	$scope.vehicle = {
		'vehicle_no': '',
		'plate_no': '',
		'condition': '',
		'vehicle_type': '',
		'color': '',
		'meter_reading': '',
		'insurance_type': '',
		'insurance_value': '',
		'vehicle_make': '',
	}
	$scope.change_type = false;
	$scope.init = function(csrf_token, id) {
		$scope.csrf_token = csrf_token;
		$scope.vehicle_id = id;
		get_vehicle_types($scope, $http);
		$scope.get_vehicle_details();
	}

	$scope.add_new_type = function() {
		if ($scope.vehicle.vehicle_type == 'other') {
			$scope.message = '';
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
		save_vehicle_type($scope, $http);
	}
	$scope.get_vehicle_details = function() {
		var url = '/edit_vehicle/'+$scope.vehicle_id+'/';
		$http.get(url).success(function(data){
			$scope.vehicle = data.vehicle[0];
		})
	}
	$scope.change_vehicle_type = function() {
		$scope.change_type = true;
	}
	
	$scope.edit_vehicle = function() {
		$scope.is_valid = validate_vehicle_form($scope, $http);
		if ($scope.is_valid) {
			$scope.validation_error = '';
			params = {
				'vehicle_details': angular.toJson($scope.vehicle),
				"csrfmiddlewaretoken" : $scope.csrf_token,
			}
			var url = "/edit_vehicle/"+ $scope.vehicle_id+'/';
			console.log(url);
			$http({
                method : 'post',
                url : url,
                data : $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data, status) {
                document.location.href ='/vehicles/';
            }).error(function(data, status){
                $scope.validation_error = data.message;
            });
		}
	}
}

function EditClientController($scope, $http, $location) {
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
	$scope.init = function(csrf_token, client_id) {
		$scope.csrf_token = csrf_token;
		$scope.client_id = client_id;
		$scope.get_client_details();
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
	$scope.get_client_details = function() {
		var url = '/edit_client/'+$scope.client_id+'/';
		$http.get(url).success(function(data){
			$scope.client = data.client[0];
			$scope.home_address = data.client[0].home_address;
			$scope.work_address = data.client[0].work_address;
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

	$scope.edit_client = function() {
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
            var url = '/edit_client/'+$scope.client_id+'/';
            $http({
                method : 'post',
                url : url,
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

function RentAgreementController($scope, $http, $location) {

	$scope.client = {
		'id': '',
		'client_name': '',
		'license_no': '',
		'license_issue_date': '',
		'license_type': '',
		'expiry_date': '',
		'passport_no': '',
		'passport_date_of_issue': '',
	}
	$scope.vehicle = {
		'id': '',
		'vehicle_no': '',
		'plate_no': '',
		'vehicle_condition': '',
		'type_of_insuranse': '',
		'insuranse_value': '',
		'meter_reading': '',
	}
	$scope.rent_agreement = {
		'client_id': '',
		'vehicle_id': '',
		'agreement_no': '',
		'agreement_type': '',
		'rent_type': '',
		'amount': 0,
		'date': '',
		'commission': 0,
		'start_date_time': '',
		'reduction': 0,
		'end_date_time': '',
		'rent': 0,
		'paid': 0,
		'balance': 0,
		'type_of_contract': '',
		'with_driver': 'no',
		'driver_name': '',
		'driver_phone': '',
		'driver_address': '',
		'passport_no': '',
		'nationality': '',
		'license_no': '',
		'dob': '',
		'license_expiry_date': '',
		'license_issued_place': '',
		'license_issued_date': '',
		'sponsar_name': '',
		'sponsar_telephone': '',
		'sponsar_address': '',
		'notes': '',
	}
	$scope.driver_details_needed = true;
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
		get_clients($scope, $http);
		get_vehicles($scope, $http);
		
        new Picker.Date($$('#date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
            canAlwaysGoUp: ['months', 'years']
        });
        
        new Picker.Date($$('#start_date_time'), {
            timePicker: true,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y %H:%M',
            canAlwaysGoUp: ['months', 'years']
        });
        new Picker.Date($$('#end_date_time'), {
            timePicker: true,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y %H:%M',
            canAlwaysGoUp: ['months', 'years']
        });
        new Picker.Date($$('#dob'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
            canAlwaysGoUp: ['months', 'years']
        });
        new Picker.Date($$('#passport_issued_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
            canAlwaysGoUp: ['months', 'years']
        });
      	new Picker.Date($$('#expiry_date'), {
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
            canAlwaysGoUp: ['months', 'years']
        });

	}
	$scope.add_new_vehicle = function() {
		$scope.vehicle = {
			'vehicle_no': '',
			'plate_no': '',
			'condition': '',
			'vehicle_type': '',
			'color': '',
			'meter_reading': '',
			'insurance_type': '',
			'insurance_value': '',
			'vehicle_make': '',
		}
		$scope.message = '';
		$scope.popup = new DialogueModelWindow({
            'dialogue_popup_width': '36%',
            'message_padding': '0px',
            'left': '28%',
            'top': '40px',
            'height': 'auto',
            'content_div': '#new_vehicle'
        });
        var height = $(document).height();
        $scope.popup.set_overlay_height(height);
        $scope.popup.show_content();
        get_vehicle_types($scope, $http);
	}
	$scope.add_new_type = function() {
		
		if ($scope.vehicle.vehicle_type == 'other') {
			$('#new_vehicle').hide();
			$scope.message = '';
			$scope.type_popup = new DialogueModelWindow({
                'dialogue_popup_width': '36%',
                'message_padding': '0px',
                'left': '28%',
                'top': '40px',
                'height': 'auto',
                'content_div': '#new_vehicle_type'
            });
            var height = $(document).height();
            $scope.type_popup.set_overlay_height(height);
            $scope.type_popup.show_content();
		}
	}
	$scope.close_popup = function() {
		// $scope.type_popup.hide_popup();
		$('#new_vehicle_type').hide();
		$('#new_vehicle').show();
	}
	$scope.add_client = function() {
		$scope.client_popup = new DialogueModelWindow({
            'dialogue_popup_width': '36%',
            'message_padding': '0px',
            'left': '28%',
            'top': '40px',
            'height': 'auto',
            'content_div': '#new_client'
        });
        var height = $(document).height();
        $scope.client_popup.set_overlay_height(height);
        $scope.client_popup.show_content();
	}
	$scope.save_client = function() {
		add_client($scope, $http, 'client_popup');
	}
 
	$scope.close_popup_add_client = function() {
		$scope.client_popup.hide_popup();
	}
	$scope.close_popup_add_vehicle =  function() {
		$scope.popup.hide_popup();
	}
	$scope.save_new_vehicle_type = function() {
		save_vehicle_type($scope, $http, 'add_vehicle');
	}
	$scope.get_customer_details = function(client) {
		$scope.client = client;
		$scope.rent_agreement.client_id = $scope.client.id;
	}
	$scope.get_vehicle_details = function(vehicle) {
		$scope.vehicle = vehicle;
		$scope.rent_agreement.vehicle_id = $scope.vehicle.id;
	}
	$scope.save_vehicle = function() {
		add_vehicle($scope, $http, 'add_vehicle');
	}


	$scope.with_driver_mode = function(mode) {
		if (mode == 'yes') {
			$scope.driver_details_needed = false;
			new Picker.Date($$('#driver_dob'), {
	            timePicker: false,
	            positionOffset: {x: 5, y: 0},
	            pickerClass: 'datepicker_bootstrap',
	            useFadeInOut: !Browser.ie,
	            format:'%d/%m/%Y',
	            canAlwaysGoUp: ['months', 'years']
	        });
			new Picker.Date($$('#license_expiry_date'), {
	            timePicker: false,
	            positionOffset: {x: 5, y: 0},
	            pickerClass: 'datepicker_bootstrap',
	            useFadeInOut: !Browser.ie,
	            format:'%d/%m/%Y',
	            canAlwaysGoUp: ['months', 'years']
	        });
	        new Picker.Date($$('#license_issued_date'), {
	            timePicker: false,
	            positionOffset: {x: 5, y: 0},
	            pickerClass: 'datepicker_bootstrap',
	            useFadeInOut: !Browser.ie,
	            format:'%d/%m/%Y',
	            canAlwaysGoUp: ['months', 'years']
	        });
		} else {
			$scope.driver_details_needed = true;
		}
	}
	$scope.calculate_rent_amount = function() {
		if ($scope.rent_agreement.amount != Number($scope.rent_agreement.amount) || $scope.rent_agreement.amount == '') {
			$scope.rent_agreement.amount = 0;
		}
		if ($scope.rent_agreement.commission != Number($scope.rent_agreement.commission) || $scope.rent_agreement.commission == '') {
			$scope.rent_agreement.commission = 0;
		}
		if ($scope.rent_agreement.reduction != Number($scope.rent_agreement.reduction) || $scope.rent_agreement.reduction == '') {
			$scope.rent_agreement.reduction = 0;
		}
		if ($scope.rent_agreement.paid != Number($scope.rent_agreement.paid) || $scope.rent_agreement.paid == '') {
			$scope.rent_agreement.paid = 0;
		}
		$scope.rent_agreement.rent = ((parseFloat($scope.rent_agreement.amount) + parseFloat($scope.rent_agreement.commission)) - parseFloat($scope.rent_agreement.reduction)).toFixed(2);
		$scope.rent_agreement.balance = (parseFloat($scope.rent_agreement.rent) - parseFloat($scope.rent_agreement.paid)).toFixed(2);
	}
	$scope.rent_agreement_validation = function() {

		$scope.rent_agreement.agreement_no = $$('#agreement_no')[0].get('value');
		$scope.rent_agreement.dob = $$('#dob')[0].get('value');
		$scope.rent_agreement.date = $$('#date')[0].get('value');
		$scope.rent_agreement.license_expiry_date = $$('#license_expiry_date')[0].get('value'); 
		$scope.rent_agreement.license_issued_date = $$('#license_issued_date')[0].get('value');
		$scope.rent_agreement.start_date_time = $$('#start_date_time')[0].get('value');
		$scope.rent_agreement.end_date_time = $$('#end_date_time')[0].get('value');
		
		if ($scope.rent_agreement.agreement_no == '' || $scope.rent_agreement.agreement_no == undefined) {
			$scope.validation_error = 'Please enter the Agreement No.';
			return false;
		} else if ($scope.rent_agreement.agreement_type == '' || $scope.rent_agreement.agreement_type == undefined) {
			$scope.validation_error = 'Please enter the Agreement Type';
			return false;
		} else if ($scope.client.id == '' || $scope.client.id == undefined) {
			$scope.validation_error = 'Please choose the Customer';
			return false;
		} else if ($scope.vehicle.id == '' || $scope.vehicle.id == undefined) {
			$scope.validation_error = 'Please choose the Vehicle';
			return false;
		} else if ($scope.rent_agreement.rent_type == '' || $scope.rent_agreement.rent_type == undefined) {
			$scope.validation_error = 'Please enter the Rent Type';
			return false;
		} else if ($scope.rent_agreement.date == '' || $scope.rent_agreement.date == undefined) { 
			$scope.validation_error = 'Please enter the Agreement Date';
			return false;
		} else if ($scope.rent_agreement.start_date_time == '' || $scope.rent_agreement.start_date_time == undefined) {
			$scope.validation_error = 'Please enter the Starting Date and Time';
			return false;
		} else if ($scope.rent_agreement.end_date_time == '' || $scope.rent_agreement.end_date_time == undefined) {
			$scope.validation_error = 'Please enter the End Date and Time';
			return false;
		} else if ($scope.rent_agreement.amount == 0 || $scope.rent_agreement.amount == undefined) {
			$scope.validation_error = 'Please enter the Amount';
			return false;
		} else if ($scope.rent_agreement.paid == undefined || $scope.rent_agreement.paid == '') {
			$scope.validation_error = 'Please enter the Paid';
			return false;
		} else if ($scope.rent_agreement.type_of_contract == '' || $scope.rent_agreement.type_of_contract == undefined) {
			$scope.validation_error = 'Please enter Type of Contract';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.driver_name == '' || $scope.rent_agreement.driver_name == undefined)) {
			$scope.validation_error = 'Please enter Driver name';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.driver_phone == '' || $scope.rent_agreement.driver_phone == undefined)) {
			$scope.validation_error = 'Please enter Driver Phone';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.driver_address == '' || $scope.rent_agreement.driver_address == undefined)) {
			$scope.validation_error = 'Please enter Driver Address';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.passport_no == '' || $scope.rent_agreement.passport_no == undefined)) {
			$scope.validation_error = 'Please enter Passport No.';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.nationality == '' || $scope.rent_agreement.nationality == undefined)) {
			$scope.validation_error = 'Please enter Nationality';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.license_no == '' || $scope.rent_agreement.license_no == undefined)) {
			$scope.validation_error = 'Please enter License No.';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.dob == '' || $scope.rent_agreement.dob == undefined)) {
			$scope.validation_error = 'Please enter Date of Birth';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.license_expiry_date == '' || $scope.rent_agreement.license_expiry_date == undefined)) {
			$scope.validation_error = 'Please enter License Expiry Date';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.license_issued_place == '' || $scope.rent_agreement.license_issued_place == undefined)) {
			$scope.validation_error = 'Please enter License Issued Place';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.license_issued_date == '' || $scope.rent_agreement.license_issued_date == undefined)) {
			$scope.validation_error = 'Please enter License Issued Date';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.sponsar_name == '' || $scope.rent_agreement.sponsar_name == undefined)) {
			$scope.validation_error = 'Please enter Sponsar Name';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.sponsar_telephone == '' || $scope.rent_agreement.sponsar_telephone == undefined)) {
			$scope.validation_error = 'Please enter Sponsar Telephone';
			return false;
		} else if ($scope.rent_agreement.with_driver == 'yes' && ($scope.rent_agreement.sponsar_address == '' || $scope.rent_agreement.sponsar_address == undefined)) {
			$scope.validation_error = 'Please enter Sponsar Address';
			return false;
		} 
		return true;
	}  
	$scope.create_rent_agreement = function() {
		$scope.is_valid = $scope.rent_agreement_validation();
		params = {
			"csrfmiddlewaretoken": $scope.csrf_token,
			'rent_agreement': angular.toJson($scope.rent_agreement),
		}
		if ($scope.is_valid) {
			$http({
	            method : 'post',
	            url : '/rent_agreement/',
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
	                document.location.href ='/rent_agreement/';
	                console.log('added');
	            }
	        }).error(function(data, status){
	            $scope.validation_error = data.message;
	            console.log('error occured');
	        });
	    }
	}
}

function ReceiveCarController($scope, $http, $location) {
	$scope.agreement = {
		'id': '',
		'client': '',
		'vehicle_no': '',
		'agreement_no': '',
		'agreement_type': '',
		'begining_date': '',
		'begining_time': '',
		'end_date': '',
		'end_time': '',
		'vehicle_condition': '',
		'insurance_value': '',
		'insurance_type': '',
		'meter_reading': '',
		'plate_no': '',
		'date': '',
		'rent': 0,
		'paid': 0,
		'type_of_contract': '',
		'with_driver': 'no',
		'driver_name': '',
		'driver_phone': '',
		'driver_address': '',
		'passport_no': '',
		'nationality': '',
		'license_no': '',
		'dob': '',
		'passport_no': '',
		'place_of_issue': '',
		'license_date': '',
		'license_type': '',
		'sponsar_name': '',
		'sponsar_telephone': '',
		'sponsar_address': '',
		'notes': '',
		'late_message': '',
	}
	$scope.receipt = {
		'receipt_no': '',
		'agreement_id': '',
		'receipt_date': '',
		'credit_card_no': '',
		'card_expiry_date': '',
		'cheque_no': '',
		'meter_reading': 0,
		'petrol': 0,
		'fine': 0,
		'accident_passable': 0,
		'extra_charge': 0,
		'total_amount': 0,
		'reduction': 0,
		'balance': 0,
		'paid': 0,
		'notes': '',
	}
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
		new Picker.Date($$('#card_expiry_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            pickOnly: 'months',
            format:'%m/%Y',
        });
        new Picker.Date($$('#receipt_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
	}
	$scope.get_agreement_details = function() {
		var url = '/agreements/?agreement_no='+$scope.contract_no;
		$http.get(url).success(function(data) {
			console.log(data.agreements.length);
			if (data.agreements.length == 0) {
				$scope.message = 'No Rent Agreement with this  Agreement No.';
				$scope.agreement_selected = true;
			} else {
				$scope.message = '';
				$scope.agreements = data.agreements;
				$scope.selecting_agreement = true;
				$scope.agreement_selected = false;
			}
		})
	}
	$scope.add_agreement = function(agreement) {
		$scope.agreement = agreement;
		$scope.contract_no = agreement.agreement_no;
		$scope.agreement_selected = true;
		$scope.receipt.total_amount = agreement.rent;
		$scope.receipt.agreement_id = agreement.id;
		$scope.calculate_balance();
	}
	$scope.calculate_balance = function() {
		if ($scope.receipt.petrol == '' || $scope.receipt.petrol != Number($scope.receipt.petrol)) {
			$scope.receipt.petrol = 0;
		}
		if ($scope.agreement.rent == '' || $scope.agreement.rent != Number($scope.agreement.rent)) {
			$scope.agreement.rent = 0;
		}
		if ($scope.receipt.fine == '' || $scope.receipt.fine != Number($scope.receipt.fine)) {
			$scope.receipt.fine =  0;
		}
		if ($scope.receipt.accident_passable == '' || $scope.receipt.accident_passable != Number($scope.receipt.accident_passable)) {
			$scope.receipt.accident_passable = 0;
		}
		if ($scope.receipt.extra_charge == '' || $scope.receipt.extra_charge != Number($scope.receipt.extra_charge)) {
			$scope.receipt.extra_charge = 0;
		}
		if ($scope.receipt.reduction == '' || $scope.receipt.reduction != Number($scope.receipt.reduction)) {
			$scope.receipt.reduction = 0;
		}
		if ($scope.receipt.paid == '' || $scope.receipt.paid != Number($scope.receipt.paid)) {
			$scope.receipt.paid = 0;
		}
		$scope.receipt.total_amount = (parseFloat($scope.agreement.rent) + parseFloat($scope.receipt.petrol) + parseFloat($scope.receipt.fine) + parseFloat($scope.receipt.accident_passable) + parseFloat($scope.receipt.extra_charge)).toFixed(2);
		$scope.receipt.total_amount = (parseFloat($scope.receipt.total_amount) - parseFloat($scope.receipt.reduction)).toFixed(2);
		$scope.receipt.balance = (parseFloat($scope.receipt.total_amount) - parseFloat($scope.agreement.paid)).toFixed(2);
		$scope.receipt.balance = parseFloat($scope.receipt.balance) - parseFloat($scope.receipt.paid);
	}

	$scope.receipt_car_validation = function() {
		$scope.receipt.receipt_date = $$('#receipt_date')[0].get('value');
		$scope.receipt.card_expiry_date = $$('#card_expiry_date')[0].get('value');
		$scope.receipt.receipt_no = $$('#receipt_no')[0].get('value');
		if ($scope.receipt.agreement_id == '' || $scope.receipt.agreement_id == undefined) {
			$scope.validation_error = 'Please enter Contract No.';
			return false;
		} else if ($scope.receipt.receipt_date == '' || $scope.receipt.receipt_date == undefined) {
			$scope.validation_error = 'Please choose Receipt Date';
			return false;
		} else if (($scope.receipt.credit_card_no == '' || $scope.receipt.credit_card_no == undefined) && ($scope.receipt.cheque_no == '' || $scope.receipt.cheque_no == undefined)) {
			$scope.validation_error = 'Please enter Credit Card No or Cheque No';
			return false;
		} else if ($scope.receipt.credit_card_no != '' && ($scope.receipt.card_expiry_date == '' || $scope.receipt.card_expiry_date == undefined)) {
			$scope.validation_error = 'Please enter Credit Card Expiry Date';
			return false;
		} else if ($scope.receipt.meter_reading == 0 || $scope.receipt.meter_reading == '' || $scope.receipt.meter_reading == undefined) {
			$scope.validation_error = 'Please enter Meter Reading';
			return false;
		} else if ($scope.receipt.paid == 0 || $scope.receipt.paid == '' || $scope.receipt.paid == undefined) {
			$scope.validation_error = 'Please enter Paid Amount on Receipt';
			return false;
		}
		return true;
	}

	$scope.receipt_car = function() {
		$scope.is_valid = $scope.receipt_car_validation();
		console.log($scope.is_valid);
		params = {
			'receipt_car': angular.toJson($scope.receipt),
			'csrfmiddlewaretoken': $scope.csrf_token,
		}
		if ($scope.is_valid) {
			$http({
	            method : 'post',
	            url : '/receive_car/',
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
	                // document.location.href ='/receive_car/';
	                console.log('added');
	            }
	        }).error(function(data, status){
	            $scope.validation_error = data.message;
	            console.log('error occured');
	        });
		}
	}
}


