

function AddClientController($scope, $http, $location) {

	$scope.client = {
		'name': '',
		'nationality': '',
		'dob': '',
		// 'home_address': '',
		'home_ph_no': '',
		// 'work_address': '',
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