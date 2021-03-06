
get_vehicle_types = function($scope, $http) {
	$http.get('/vehicle_type/list/').success(function(data){
		$scope.vehicle_types = data.vehicle_types;
	})
}

get_vehicles = function($scope, $http, list_type) {
	$http.get('/vehicles/').success(function(data){
		if (list_type != 'whole_vehicle_list') {
			$scope.vehicles = data.vehicles;
		} else {
			$scope.vehicles = data.whole_vehicles;
		}
	})
}

get_case_types = function($scope, $http) {
	$http.get('/case_types/').success(function(data){
		$scope.case_types = data.case_types;
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
	console.log(Number($scope.vehicle.petrol));
	if ($scope.vehicle.insurance_value == '' || $scope.vehicle.insurance_value == undefined) {
		$scope.vehicle.insurance_value = 0;
	}
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
	} else if (!Number($scope.vehicle.meter_reading)) {
		$scope.validation_error = 'Please enter a Valid Meter Reading';
		return false;
	} else if ($scope.vehicle.petrol != Number($scope.vehicle.petrol)) {
		$scope.validation_error = 'Please enter a Valid Petrol';
		return false;
	} else if ($scope.vehicle.insurance_value && (!Number($scope.vehicle.insurance_value))) {
		$scope.validation_error = 'Please enter a Valid Insurance Value';
		return false;
	}
	return true;
}
add_vehicle = function($scope, $http, from) {
	$scope.is_valid = validate_vehicle_form($scope, $http);
	if ($scope.is_valid) {
		var height = $(document).height();
        height = height + 'px';
        $('#overlay').css('height', height);
        $('#spinner').css('height', height);
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
        		$('#overlay').css('height', '0px');
        	}
	       $('#spinner').css('height', '0px');
        	if (data.result == 'error') {
        		$scope.validation_error = data.message;
        	} else {
	            if (from != 'add_vehicle') {
	            	document.location.href ='/vehicles/';
	            } else {
	            	$scope.vehicle_data = data.vehicle_data[0];
	            	get_vehicles($scope, $http, '');
	            	$scope.vehicle = data.vehicle_data[0];
	            	$scope.rent_agreement.vehicle_id = $scope.vehicle.id;
	            	$scope.close_popup_add_vehicle();
	            }
	        }
        }).error(function(data, status){
	        $('#overlay').css('height', '0px');
	        $('#spinner').css('height', '0px');
            $scope.validation_error = data.message;
        });
	}
}

validate_driver_form = function($scope, $http, from) {
	if (from != 'add_driver') {
		$scope.driver.dob = $$('#dob')[0].get('value');
		$scope.driver.date_of_license_issue =  $$('#date_of_license_issue')[0].get('value');
		$scope.driver.passport_issued_date =  $$('#passport_issued_date')[0].get('value');
		$scope.driver.expiry_date = $$('#expiry_date')[0].get('value');
	} else {
		$scope.driver.dob = $$('#driver_dob')[0].get('value');
		$scope.driver.date_of_license_issue =  $$('#driver_license_issue')[0].get('value');
		$scope.driver.expiry_date = $$('#driver_license_expiry_date')[0].get('value');
		$scope.driver.passport_issued_date =  $$('#passportissued_date')[0].get('value');
	}
	if ($scope.driver.name == '' || $scope.driver.name == undefined) {
		$scope.validation_error = 'Please enter Name';
		return false;
	} else if ($scope.driver.nationality == '' || $scope.driver.nationality == undefined) {
		$scope.validation_error = 'Please enter Nationality';
		return false;
	} else if ($scope.driver.dob == '' || $scope.driver.dob == undefined) {
		$scope.validation_error = 'Please enter Date of Birth';
		return false;
	} else if ($scope.home_address == '' || $scope.home_address == undefined) {
		$scope.validation_error = 'Please enter Home Address';
		return false;
	} else if ($scope.driver.home_ph_no == '' || $scope.driver.home_ph_no == undefined) {
		$scope.validation_error = 'Please enter Home Phone No';
		return false;
	} else if ($scope.driver.license_no == '' || $scope.driver.license_no == undefined) {
		$scope.validation_error = 'Please enter License No';
		return false;
	} else if ($scope.driver.license_type == '' || $scope.driver.license_type == undefined) {
		$scope.validation_error = 'Please choose License Type';
		return false;
	} else if ($scope.driver.date_of_license_issue == '' || $scope.driver.date_of_license_issue == undefined) {
		$scope.validation_error = 'Please enter Date of License Issued';
		return false;
	} else if ($scope.driver.issued_place == '' || $scope.driver.issued_place == undefined) {
		$scope.validation_error = 'Please enter Issued Place';
		return false;
	} else if ($scope.driver.expiry_date == '' || $scope.driver.expiry_date == undefined) {
		$scope.validation_error = 'Please enter Expiry Date';
		return false;
	} else if ($scope.driver.emirates_id == '' || $scope.driver.emirates_id == undefined) {
		$scope.validation_error = 'Please enter Emirates Id';
		return false;
	} 
	return true;
}

add_driver = function($scope, $http, from) {
	$scope.is_valid = validate_driver_form($scope, $http, from);
	if ($scope.is_valid) {
		$scope.validation_error = '';
		params = {
			'driver_details': angular.toJson($scope.driver),
			'home_address': $scope.home_address,
			'sponsar_address': $scope.sponsar_address,
			'driver_working_address': $scope.driver_working_address,
			"csrfmiddlewaretoken" : $scope.csrf_token,
		}
		var height = $(document).height();
        height = height + 'px';
        $('#overlay').css('height', height);
        $('#spinner').css('height', height);
		$http({
            method : 'post',
            url : "/add_driver/",
            data : $.param(params),
            headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
        }).success(function(data, status) {
        	if (from != 'add_driver') {
	        	$('#overlay').css('height', '0px');
	        }
	        $('#spinner').css('height', '0px');
        	if (data.result == 'error') {
        		$scope.validation_error = data.message;
        	} else {
	            if (from != 'add_driver') {
	            	document.location.href ='/drivers/';
	            } else {
	            	$scope.driver_data = data.driver_data[0];
	            	$scope.driver = data.driver_data[0];
	            	$scope.driver_name = $scope.driver.driver_name;
	            	$scope.rent_agreement.driver_id = $scope.driver.id;
	            	$scope.close_popup_add_driver();
	            }
	        }
        }).error(function(data, status){
	        $('#overlay').css('height', '0px');
	        $('#spinner').css('height', '0px');
            $scope.validation_error = data.message;
        });
	}
}

get_agreement_details = function($scope, $http, from) {
	console.log(from);
	var url = '/agreements/?agreement_no='+$scope.contract_no;
	$http.get(url).success(function(data) {
		console.log(data.agreements.length);
		var agreement_length = 0;
		if (from == 'receive_car') {
			agreement_length = data.whole_agreements.length;
			$scope.agreement_date = data.whole_agreements.date;
		} else if (from == 'rent_agreement') {
			agreement_length = data.rent_agreements.length;
		} else {
			agreement_length = data.agreements.length;
		}
		if (agreement_length == 0) {
			$scope.message = 'No Rent Agreement with this  Agreement No.';
			$scope.agreement_selected = true;
		} else {
			$scope.message = '';
			if (from == 'receive_car') {
				$scope.agreements = data.whole_agreements;
			} else if (from == 'rent_agreement') {
				$scope.agreements = data.rent_agreements;
			} else {
				$scope.agreements = data.agreements;
			}
			$scope.selecting_agreement = true;
			$scope.agreement_selected = false;
		}
	})
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
		'insurance_value': 0,
		'vehicle_make': '',
		'petrol': '',
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
		'petrol': '',
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
            	if (data.result == 'error') {
            		$scope.validation_error = data.message;
            	} else {
                	document.location.href ='/vehicles/';
                }
            }).error(function(data, status){
                $scope.validation_error = data.message;
            });
		}
	}
}


function RentAgreementController($scope, $http, $location) {

	$scope.vehicle = {
		'id': '',
		'vehicle_no': '',
		'plate_no': '',
		'vehicle_condition': '',
		'type_of_insuranse': '',
		'insuranse_value': '',
		'meter_reading': '',
		'petrol': '',
	}
	$scope.driver = {
		'id': '',
		'driver_name': '',
		'driver_phone': '',
		'driver_address': '',
		'driver_nationality': '',
		'driver_license_no': '',
		'driver_license_issue_date': '',
		'driver_license_issue_place': '',
		'driver_license_expiry_date': '',
		'driver_dob': '',
		'sponsar_name': '',
		'sponsar_address': '',
		'sponsar_ph': '',
		'license_type': '',

	}
	$scope.rent_agreement = {
		'vehicle_id': '',
		'driver_id': '',
		'agreement_no': '',
		'rent_type': '',
		'amount': 0,
		'date': '',
		'start_date_time': '',
		'end_date_time': '',
		'rent': 0,
		'paid': 0,
		'balance': 0,
		'notes': '',
		'client_identity': '',
		'vehicle_scratch': 0,
		'accident_passable': 0,
		'rental_in_km': 0,
		'liable_to_pay_in_km': 0,
	}
	$scope.driver_details_needed = true;
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
		get_vehicles($scope, $http, '');
		// get_drivers($scope, $http);
		
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
            format:'%d/%m/%Y %X',
            canAlwaysGoUp: ['months', 'years'],
            ampm: true,
        });
        new Picker.Date($$('#end_date_time'), {
            timePicker: true,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y %X',
            canAlwaysGoUp: ['months', 'years'],
            ampm: true,
        });
        new Picker.Date($$('#dob'), {
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
			'petrol': '',
		}
		$scope.validation_error = '';
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
		$('#new_vehicle_type').hide();
		$('#new_vehicle').show();
	}
	
	$scope.add_new_driver = function() {
		$scope.validation_error = '';
		$scope.home_address = '';
		$scope.driver_working_address = '';
		$scope.rent_agreement.driver_id = '';
		$scope.driver = {
			'id': '',
			'driver_name': '',
			'driver_phone': '',
			'driver_address': '',
			'driver_nationality': '',
			'driver_license_no': '',
			'driver_license_issue_date': '',
			'driver_license_issue_place': '',
			'driver_license_expiry_date': '',
			'driver_dob': '',
			'sponsar_name': '',
			'sponsar_address': '',
			'sponsar_ph': '',
			'working_tel_no': '',
			'passport_issued_date': '',
			'place_of_issue': '',
		}
		$scope.driver_popup = new DialogueModelWindow({
            'dialogue_popup_width': '36%',
            'message_padding': '0px',
            'left': '28%',
            'top': '40px',
            'height': 'auto',
            'content_div': '#new_driver'
        });
        new Picker.Date($$('#driver_dob'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
            canAlwaysGoUp: ['months', 'years']
        });
        new Picker.Date($$('#driver_license_expiry_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
            canAlwaysGoUp: ['months', 'years']
        });
      	new Picker.Date($$('#driver_license_issue'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
            canAlwaysGoUp: ['months', 'years']
        });
        new Picker.Date($$('#passportissued_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        var height = $(document).height();
        $scope.driver_popup.set_overlay_height(height);
        $scope.driver_popup.show_content();
	}
	$scope.get_driver_details = function(){
		$scope.rent_agreement.driver_id = '';
		$scope.driver = {
			'id': '',
			'driver_name': '',
			'driver_phone': '',
			'driver_address': '',
			'driver_nationality': '',
			'driver_license_no': '',
			'driver_license_issue_date': '',
			'driver_license_issue_place': '',
			'driver_license_expiry_date': '',
			'driver_dob': '',
			'sponsar_name': '',
			'sponsar_address': '',
			'sponsar_ph': '',
			'working_tel_no': '',
			'passport_issued_date': '',
			'place_of_issue': '',
		}
		var url = '/drivers/?driver_name=' + $scope.driver_name; 
		$http.get(url).success(function(data){
			if (data.drivers.length == 0) {
				$scope.driver_message = 'No driver with this name';
				$scope.drivers = [];
				$scope.driver_selected = true;
			} else {
				$scope.driver_message = '';
				$scope.drivers = data.drivers;
				$scope.selecting_driver = true;
				$scope.driver_selected = false;
			}
			
		})
	}
	$scope.add_driver = function(driver){
		$scope.driver_selected = true;
		$scope.rent_agreement.driver_id = driver.id;
		$scope.driver = {
			'id': '',
			'driver_name': '',
			'driver_phone': '',
			'driver_address': '',
			'driver_nationality': '',
			'driver_license_no': '',
			'driver_license_issue_date': '',
			'driver_license_issue_place': '',
			'driver_license_expiry_date': '',
			'driver_dob': '',
			'sponsar_name': '',
			'sponsar_address': '',
			'sponsar_ph': '',
			'working_tel_no': '',
			'passport_issued_date': '',
			'place_of_issue': '',
		}
		$scope.driver = driver;
		$scope.driver_name = driver.driver_name;
	}
	$scope.close_popup_add_vehicle =  function() {
		$scope.popup.hide_popup();
	}
	$scope.save_new_vehicle_type = function() {
		save_vehicle_type($scope, $http, 'add_vehicle');
	}
	
	$scope.get_vehicle_details = function(vehicle) {
		$scope.vehicle = vehicle;
		$scope.rent_agreement.vehicle_id = $scope.vehicle.id;
	}
	$scope.save_vehicle = function() {
		add_vehicle($scope, $http, 'add_vehicle');
	}
	$scope.save_driver = function() {
		add_driver($scope, $http, 'add_driver');
	}
	$scope.close_popup_add_driver =function() {
		$scope.driver_popup.hide_popup();
	}
	$scope.calculate_rent_amount = function() {
		if ($scope.rent_agreement.amount != Number($scope.rent_agreement.amount) || $scope.rent_agreement.amount == '') {
			$scope.rent_agreement.amount = 0;
		}
		
		if ($scope.rent_agreement.paid != Number($scope.rent_agreement.paid) || $scope.rent_agreement.paid == '') {
			$scope.rent_agreement.paid = 0;
		}
		$scope.rent_agreement.rent = (parseFloat($scope.rent_agreement.amount)).toFixed(2);
		$scope.rent_agreement.balance = (parseFloat($scope.rent_agreement.rent) - parseFloat($scope.rent_agreement.paid)).toFixed(2);
	}
	$scope.rent_agreement_validation = function() {

		$scope.rent_agreement.agreement_no = $$('#agreement_no')[0].get('value');
		$scope.rent_agreement.dob = $$('#driver_dob')[0].get('value');
		$scope.rent_agreement.date = $$('#date')[0].get('value');
		$scope.rent_agreement.license_issued_date = $$('#license_issued_date')[0].get('value');
		$scope.rent_agreement.start_date_time = $$('#start_date_time')[0].get('value');
		$scope.rent_agreement.end_date_time = $$('#end_date_time')[0].get('value');
		console.log($scope.rent_agreement.rental_in_km, !Number($scope.rent_agreement.rental_in_km));
		if ($scope.rent_agreement.agreement_no == '' || $scope.rent_agreement.agreement_no == undefined) {
			$scope.validation_error = 'Please enter the Agreement No.';
			return false;
		} else if ($scope.rent_agreement.driver_id == '' || $scope.rent_agreement.driver_id == undefined) {
			$scope.validation_error = 'Please choose Driver name';
			return false;
		} else if ($scope.rent_agreement.client_identity == '' || $scope.rent_agreement.client_identity == undefined) {
			$scope.validation_error = 'Please choose the Driver Identity';
			return false;
		} else if ($scope.vehicle.id == '' || $scope.vehicle.id == undefined) {
			$scope.validation_error = 'Please choose the Vehicle';
			return false;
		} else if ($scope.vehicle.meter_reading !=0 && (!Number($scope.vehicle.meter_reading))) {
			$scope.validation_error = 'Please enter valid Meter Reading';
			return false;
		} else if ($scope.rent_agreement.rental_in_km != 0 && (!Number(parseFloat($scope.rent_agreement.rental_in_km)))) {
			$scope.validation_error = 'Please enter valid Rental Entitled in KM';
			return false;
		} else if ($scope.rent_agreement.liable_to_pay_in_km !=0 && (!Number($scope.rent_agreement.liable_to_pay_in_km))) {
			$scope.validation_error = 'Please enter valid Liable to Pay in KM';
			return false;
		} else if ($scope.rent_agreement.accident_passable !=0 &&((!Number($scope.rent_agreement.accident_passable)))) {
			$scope.validation_error = 'Please enter valid Accident Passable';
			return false;
		} else if ($scope.rent_agreement.vehicle_scratch !=0 &&((!Number($scope.rent_agreement.vehicle_scratch)))) {
			$scope.validation_error = 'Please enter valid Vehicle Scratch';
			return false;
		} else if ($scope.rent_agreement.date == '' || $scope.rent_agreement.date == undefined) { 
			$scope.validation_error = 'Please enter the Agreement Date';
			return false;
		} else if ($scope.rent_agreement.start_date_time == '' || $scope.rent_agreement.start_date_time == undefined) {
			$scope.validation_error = 'Please enter the Starting Date and Time';
			return false;
		} else if ($scope.rent_agreement.end_date_time == '' || $scope.rent_agreement.end_date_time == undefined) {
			$scope.validation_error = 'Please enter the Expected Return Date and Time';
			return false;
		} else if ($scope.rent_agreement.amount == 0 || $scope.rent_agreement.amount == undefined) {
			$scope.validation_error = 'Please enter the Amount';
			return false;
		} else if ($scope.rent_agreement.paid == undefined || $scope.rent_agreement.paid == '') {
			$scope.validation_error = 'Please enter the Deposit';
			return false;
		} else if ($scope.rent_agreement.balance < 0) {
			$scope.validation_error = 'Please enter valid Deposit';
			return false;
		}
		return true;
	}  
	$scope.create_rent_agreement = function() {
		$scope.is_valid = $scope.rent_agreement_validation();
		params = {
			"csrfmiddlewaretoken": $scope.csrf_token,
			'rent_agreement': angular.toJson($scope.rent_agreement),
			'vehicle_meter_reading': $scope.vehicle.meter_reading,
		}
		if ($scope.is_valid) {
			var height = $(document).height();
	        height = height + 'px';
	        $('#overlay').css('height', height);
	        $('#spinner').css('height', height);
			$http({
	            method : 'post',
	            url : '/rent_agreement/',
	            data : $.param(params),
	            headers : {
	                'Content-Type' : 'application/x-www-form-urlencoded'
	            }
	        }).success(function(data, status) {
	            $('#overlay').css('height', '0px');
            	$('#spinner').css('height', '0px');
	            if (data.result == 'error'){
	                $scope.error_flag=true;
	                $scope.message = data.message;
	            } else {
	                $scope.error_flag=false;
	                $scope.message = '';
	                // document.location.href ='/rent_agreement/';
	                document.location.href = '/print_rent_agreement/?rent_agreement_id='+data.agreement_id;
	                console.log('added');
	            }
	        }).error(function(data, status){
	        	$('#overlay').css('height', '0px');
	            $('#spinner').css('height', '0px');
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
		'petrol': '',
	}
	$scope.receipt = {
		'receipt_no': '',
		'agreement_id': '',
		'receipt_date': '',
		'credit_card_no': '',
		'cheque_no': '',
		'meter_reading': 0,
		'petrol': 0,
		'fine': 0,
		'extra_charge': 0,
		'total_amount': 0,
		'reduction': 0,
		'balance': 0,
		'paid': 0,
		'notes': '',
		'returning_petrol': 0,
		'salik_charges': 0,
	}
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
		$scope.test = 2;
        new Picker.Date($$('#receipt_date'), {
            timePicker: true,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y %X',
            canAlwaysGoUp: ['months', 'years'],
            ampm: true,
        });
        // new Picker.Date($$('#returning_date'), {
        //     timePicker: true,
        //     positionOffset: {x: 5, y: 0},
        //     pickerClass: 'datepicker_bootstrap',
        //     useFadeInOut: !Browser.ie,
        //     format:'%d/%m/%Y %X',
        //     canAlwaysGoUp: ['months', 'years'],
        //     ampm: true,
        //   //   onSelect: function() {
		      //  	// $scope.calculate_date_difference();
		      //  	// $scope.calculate_balance()
		      //  	// console.log($scope.receipt.total_amount ); 
		      //   // },

        // });
        
        // $scope.receipt.returning_date = $$('#returning_date')[0].get('value');
        
	}
	// $scope.$watch('datepicker',function(){
	// 		console.log("hi")
	// 		$scope.calculate_balance();
	// 	});
	$scope.calculate_date_difference = function(){
		var dt1 = $scope.agreement.begining_date.split('/');
		var one = new Date(dt1[2], dt1[1], dt1[0]);
		if ($$('#returning_date')[0].get('value') == ''){
	   		var dt2 = $scope.agreement.end_date.split('/');
	   		var two = new Date(dt2[2], dt2[1], dt2[0]);
	   	}
	   	else{
	   		var	dt2 = $$('#returning_date')[0].get('value').split('/');
	   		var year = dt2[2].split(' ')[0];
	   		var two = new Date(year, dt2[1], dt2[0]);
	   		
	   	}
	   	console.log(dt2, dt1) ;
	    
        var millisecondsPerDay = 1000 * 60 * 60 * 24;
        var millisBetween = two.getTime() - one.getTime();
        var days = millisBetween / millisecondsPerDay;
        console.log(days)
        if (days > 0){
	        $scope.receipt.total_amount = (parseFloat($scope.agreement.rent) + parseFloat($scope.receipt.petrol) + parseFloat($scope.receipt.fine) + parseFloat($scope.receipt.extra_charge) + parseFloat($scope.receipt.salik_charges)).toFixed(2);
	        $scope.receipt.total_amount = parseFloat($scope.receipt.total_amount) * days;
	        $scope.receipt.balance = (parseFloat($scope.receipt.total_amount) - parseFloat($scope.agreement.paid)).toFixed(2);
        }else{
        	$scope.receipt.total_amount = parseFloat($scope.agreement.rent);
        	$scope.receipt.balance = (parseFloat($scope.receipt.total_amount) - parseFloat($scope.agreement.paid)).toFixed(2);	
        }
	}
	$scope.get_agreement_details = function() {
		
		get_agreement_details($scope, $http,'');
	}
	$scope.add_agreement = function(agreement) {
		$scope.agreement = agreement;
		$scope.contract_no = agreement.agreement_no;
		$scope.agreement_selected = true;
		$scope.receipt = {
			'receipt_no': '',
			'agreement_id': '',
			'receipt_date': '',
			'credit_card_no': '',
			'cheque_no': '',
			'meter_reading': 0,
			'petrol': 0,
			'fine': 0,
			'extra_charge': 0,
			'total_amount': 0,
			'reduction': 0,
			'balance': 0,
			'paid': 0,
			'notes': '',
			'returning_petrol': 0,
			'returning_date': ''
		}
		$scope.receipt.total_amount = agreement.rent;
		$scope.receipt.agreement_id = agreement.id;
		$scope.receipt.rent_type = agreement.rent_type;
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
		if ($scope.receipt.salik_charges == '' || $scope.receipt.salik_charges != Number($scope.receipt.salik_charges)) {
			$scope.receipt.salik_charges = 0;
		}
		if ($scope.receipt.reduction == '' || $scope.receipt.reduction != Number($scope.receipt.reduction)) {
			$scope.receipt.reduction = 0;
		}
		if ($scope.receipt.paid == '' || $scope.receipt.paid != Number($scope.receipt.paid)) {
			$scope.receipt.paid = 0;
		}
		
		$scope.receipt.total_amount = (parseFloat($scope.agreement.rent) + parseFloat($scope.receipt.petrol) + parseFloat($scope.receipt.fine) + parseFloat($scope.receipt.extra_charge) + parseFloat($scope.receipt.salik_charges)).toFixed(2);
		if ($scope.receipt.rent_type == 'Daily' || $scope.receipt.rent_type == 'None')
			$scope.calculate_date_difference();
		$scope.receipt.total_amount = (parseFloat($scope.receipt.total_amount) - parseFloat($scope.receipt.reduction)).toFixed(2);
		$scope.receipt.balance = (parseFloat($scope.receipt.total_amount) - parseFloat($scope.agreement.paid)).toFixed(2);
		$scope.receipt.balance = parseFloat($scope.receipt.balance) - parseFloat($scope.receipt.paid);
		if ($scope.receipt.balance < 0){
			$scope.receipt.balance = 0;
			$scope.receipt.total_amount = $scope.receipt.paid;
		}
	}

	$scope.receipt_car_validation = function() {
		$scope.receipt.receipt_date = $$('#receipt_date')[0].get('value');
		$scope.receipt.returning_date = $$('#returning_date')[0].get('value');
		$scope.receipt.receipt_no = $$('#receipt_no')[0].get('value');
		if ($scope.receipt.agreement_id == '' || $scope.receipt.agreement_id == undefined) {
			$scope.validation_error = 'Please enter Contract No.';
			return false;
		} else if ($scope.receipt.receipt_date == '' || $scope.receipt.receipt_date == undefined) {
			$scope.validation_error = 'Please choose Receipt Date';
			return false;
		} else if ($scope.receipt.returning_date == '' || $scope.receipt.returning_date == undefined) {
			$scope.validation_error = 'Please choose Returning Date';
			return false;
		} else if ($scope.receipt.meter_reading == 0 || $scope.receipt.meter_reading == '' || $scope.receipt.meter_reading == undefined) {
			$scope.validation_error = 'Please enter Meter Reading on Returning';
			return false;
		} else if (!Number($scope.receipt.meter_reading)) {
			$scope.validation_error = 'Please enter valid Meter Reading on Returning';
			return false;
		} else if ($scope.receipt.returning_petrol && (!Number($scope.receipt.returning_petrol))) {
			$scope.validation_error = 'Please enter valid valid Petrol on Returning';
			return false;
		} else if ($scope.receipt.paid == 0 || $scope.receipt.paid == '' || $scope.receipt.paid == undefined) {
			$scope.validation_error = 'Please enter Paid Amount on Receipt';
			return false;
		// } else if ($scope.receipt.balance < 0) {
		// 	$scope.validation_error = 'Please enter valid Paid Amount on Receipt';
		// 	return false;
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
			var height = $(document).height();
	        height = height + 'px';
	        $('#overlay').css('height', height);
	        $('#spinner').css('height', height);
			$http({
	            method : 'post',
	            url : '/receive_car/',
	            data : $.param(params),
	            headers : {
	                'Content-Type' : 'application/x-www-form-urlencoded'
	            }
	        }).success(function(data, status) {
	            $('#overlay').css('height', '0px');
	        	$('#spinner').css('height', '0px');
	            if (data.result == 'error'){
	                $scope.error_flag=true;
	                $scope.message = data.message;
	            } else {
	                $scope.error_flag=false;
	                $scope.message = '';
	                document.location.href = '/print_receipt/?receipt_car_id='+data.receipt_id;
	            }
	        }).error(function(data, status){
        		$('#overlay').css('height', '0px');
	        	$('#spinner').css('height', '0px');
	            $scope.validation_error = data.message;
	            console.log('error occured');
	        });
		}
	}
}

function AddDriverController($scope, $http, $location) {
	$scope.driver = {
		'name': '',
		'nationality': '',
		'dob': '',
		'home_ph_no': '',
		'license_no': '',
		'date_of_license_issue': '',
		'issued_place': '',
		'expiry_date': '',
		'passport_no': '',
		'sponsar_name': '',
		'sponsar_ph': '',
		'working_tel_no': '',
		'license_type': '',
		'passport_issued_date': '',
		'place_of_issue': '',
		'emirates_id': '',
	}
	$scope.sponsar_address = '';
	$scope.home_address = '';
	$scope.driver_working_address = '';
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
		new Picker.Date($$('#dob'), {
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
        new Picker.Date($$('#date_of_license_issue'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#passport_issued_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
	}

	$scope.add_driver = function() {
		add_driver($scope, $http, '');
	}
}

function PrintReceiptCarController($scope, $http, $location){

	$scope.agreement_id = '';
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
	}
	$scope.get_agreement_details = function() {
		get_agreement_details($scope, $http, 'receive_car');
	}
	$scope.add_agreement = function(agreement) {
		$scope.agreement = agreement;
		$scope.contract_no = agreement.agreement_no;
		$scope.agreement_selected = true;
		$scope.agreement_id = agreement.id;
		
		$scope.receipt = {
			'id': '',
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
		$scope.receipt.total_amount = agreement.rent;
		$scope.receipt.agreement_id = agreement.id;
		$scope.receipt = agreement.receival_details[0];
	}
	$scope.print_receipt = function() {
		if ($scope.agreement_id == '' || $scope.agreement_id == undefined) {
			$scope.validation_error = 'Please enter Contract No';
		} else {
			document.location.href = '/print_receipt/?receipt_car_id='+$scope.receipt.id;
		}
	}

}

function PrintRentAgreementController($scope, $http, $location){

	$scope.agreement_id = '';
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
	}
	$scope.get_agreement_details = function() {
		get_agreement_details($scope, $http, 'rent_agreement');
	}
	$scope.add_agreement = function(agreement) {
		$scope.agreement = agreement;
		$scope.contract_no = agreement.agreement_no;
		$scope.agreement_selected = true;
		$scope.agreement_id = agreement.id;
	}
	$scope.print_rent_agreement = function() {
		if ($scope.agreement_id == '' || $scope.agreement_id == undefined) {
			$scope.validation_error = 'Please enter the Contract No.'
		} else {
			document.location.href = '/print_rent_agreement/?rent_agreement_id='+$scope.agreement.id;
		} 
	}
}

function CaseEntryController($scope, $http, $location) {
	$scope.case_details = {
		'client_name': '',
		'rent_agreement_id': '',
		'start_date': '',
		'end_date': '',
		'type_of_case': '',
		'fine': '',
		'penality_date': '',
		'penality_no': '',
		'date_author': '',
		'no_author': '',
		'vehicle_id': '',
		'client_id': '',
		'code_author': '',
		'ref_no': '',
		'vehicle_status': '',
	}
	$scope.init = function(csrf_token) {
		$scope.csrf_token = csrf_token;
		new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#penality_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#date_author'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        get_case_types($scope, $http);
	}
	$scope.add_case_type = function() {
		console.log($scope.case_details.type_of_case);
		if ($scope.case_details.type_of_case == 'other') {
			$scope.popup = new DialogueModelWindow({
	            'dialogue_popup_width': '36%',
	            'message_padding': '0px',
	            'left': '28%',
	            'top': '40px',
	            'height': 'auto',
	            'content_div': '#add_case_type'
	        });
	        var height = $(document).height();
	        $scope.popup.set_overlay_height(height);
	        $scope.popup.show_content();
	    }
    }
    $scope.save_case_type = function() {
    	if ($scope.case_type == '' || $scope.case_type == undefined) {
    		$scope.error_message = 'Please enter Case Type';
    	} else {
    		params = {
				'case_type': $scope.case_type,
				"csrfmiddlewaretoken" : $scope.csrf_token,
			}
			$http({
	            method : 'post',
	            url : "/add_case_type/",
	            data : $.param(params),
	            headers : {
	                'Content-Type' : 'application/x-www-form-urlencoded'
	            }
	        }).success(function(data, status) {
	        	if (data.result == 'error') {
	        		$scope.error_message = data.message;
	        	} else {
		            get_case_types($scope, $http);
		            $scope.case_details.type_of_case = data.case_name;
		            $scope.close_popup();
		        }
	        }).error(function(data, status){
	            $scope.error_message = data.message;
	        });
    	}
    }
    $scope.close_popup = function() {
    	$scope.popup.hide_popup();
    }
	$scope.get_customer_details = function() {
		$scope.case_details.start_date = $$('#start_date')[0].get('value');
		var url = '/rent_agreement_details/?start_date='+$scope.case_details.start_date+'&vehicle_no='+$scope.case_details.vehicle_no;
		$http.get(url).success(function(data) {
			if (data.client_name == '' || data.client_name == undefined) {
				$scope.case_details.client_name = data.client_name;
				$scope.validation_error = 'No such client with these details';
				$scope.case_details.vehicle_status = data.vehicle_status;
			} else {
				$scope.validation_error = '';
				$scope.case_details.client_name = data.client_name;
				$scope.case_details.client_id = data.client_id;
				$scope.case_details.vehicle_id = data.vehicle_id;
				$scope.case_details.vehicle_status = data.vehicle_status;
				$scope.case_details.ref_no = data.ref_no;
			}
		})
	}
	$scope.case_form_validation = function() {
		$scope.case_details.penality_date = $$('#penality_date')[0].get('value');
		$scope.case_details.start_date = $$('#start_date')[0].get('value');
		$scope.case_details.date_author = $$('#date_author')[0].get('value');
		if ($scope.case_details.start_date == '' || $scope.case_details.start_date == undefined) {
			$scope.validation_error = 'Please enter Start Date';
			return false;
		} else if ($scope.case_details.client_name == '' || $scope.case_details.client_name == undefined) {
			$scope.validation_error = 'Please enter Correct vehicle No';
			return false;
		} else if ($scope.case_details.type_of_case == '' || $scope.case_details.type_of_case == undefined || $scope.case_details.type_of_case == 'other') {
			$scope.validation_error = 'Please choose Type of Case';
			return false;
		} else if ($scope.case_details.fine == '' || $scope.case_details.fine == undefined || $scope.case_details.fine != Number($scope.case_details.fine)) {
			$scope.validation_error = 'Please enter Penality Amount';
			return false;
		} else if ($scope.case_details.penality_date == '' || $scope.case_details.penality_date == undefined) {
			$scope.validation_error = 'Please enter Penality Date';
			return false;
		} else if ($scope.case_details.penality_no == '' || $scope.case_details.penality_no == undefined) {
			$scope.validation_error = 'Please enter Penality No';
			return false;
		} else if ($scope.case_details.date_author == '' || $scope.case_details.date_author == undefined) {
			$scope.validation_error = 'Please enter Date Author';
			return false;
		} else if ($scope.case_details.no_author == '' || $scope.case_details.no_author == undefined) {
			$scope.validation_error = 'Please enter No Author';
			return false;
		} else if ($scope.case_details.code_author == '' || $scope.case_details.code_author == undefined) {
			$scope.validation_error = 'Please enter Code Author';
			return false;
		} 
		return true;
	}
	$scope.create_case_entry = function() {
		$scope.is_valid = $scope.case_form_validation();
		if ($scope.is_valid) {
			params = {
				'case_details': angular.toJson($scope.case_details),
				'csrfmiddlewaretoken': $scope.csrf_token,
			}
			$http({
	            method : 'post',
	            url : "/case_entry/",
	            data : $.param(params),
	            headers : {
	                'Content-Type' : 'application/x-www-form-urlencoded'
	            }
	        }).success(function(data, status) {
	        	if (data.result == 'error') {
	        		$scope.validation_error = data.message;
	        	} else {
		            document.location.href ='/case_entry/';
		        }
	        }).error(function(data, status){
	            $scope.validation_error = data.message;
	        });
	    }
	}
}

function RentReportController($scope, $http, $location) {
	$scope.report_vehicle_wise = false;   
	$scope.report_date_wise = false;
	$scope.init = function(csrf_token, report_type) {
		$scope.csrf_token = csrf_token;
		$scope.report_type = report_type;
		if ($scope.report_type == 'vehicle'){
            $scope.report_date_wise = false;
            $scope.report_vehicle_wise = true;  
            $scope.vehicle = 'select';
        } else {
        	$scope.report_date_wise = true;
            $scope.report_vehicle_wise = false;  
        }
		new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        get_vehicles($scope, $http, 'whole_vehicle_list');
	}
	$scope.get_report_type =function() {
        if($scope.report_type == 'date'){
            $scope.error_flag = false;
            $scope.report_date_wise = true;
            $scope.report_vehicle_wise = false;         
            
        } else if($scope.report_type == 'vehicle'){
            $scope.error_flag = false;
            $scope.report_date_wise = false;
            $scope.report_vehicle_wise = true;  
            $scope.vehicle = 'select';
        }
    }
}
function RevenueReportController($scope, $http, $location) {
	$scope.init = function(csrf_token, report_type) {
		$scope.csrf_token = csrf_token;
		$scope.report_type = report_type;
		new Picker.Date($$('#start_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
        new Picker.Date($$('#end_date'), {
            timePicker: false,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y',
        });
	}
}
