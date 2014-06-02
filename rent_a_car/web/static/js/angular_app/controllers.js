

function AddClientController($scope, $http, $location) {

	$scope.client = {
		'name': '',
		'nationality': '',
		'dob': '',
		'home_address': '',
		'home_ph_no': '',
		'work_address': '',
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

	$scope.add_client = function() {

	}

}