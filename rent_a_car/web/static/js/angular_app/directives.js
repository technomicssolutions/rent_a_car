'use strict';

/* Directives */

var directives = angular.module('rent_a_car.directives', []);

directives.directive('appVersion', [ 'version', function(version)
{
    return function(scope, elm, attrs)
    {
        elm.text(version);
    };
} ]);

directives.directive('datepicker', function() {
   return {
        link:function($scope, $element, $attr, $controller){
            new Picker.Date($$('#returning_date'), {
            timePicker: true,
            positionOffset: {x: 5, y: 0},
            pickerClass: 'datepicker_bootstrap',
            useFadeInOut: !Browser.ie,
            format:'%d/%m/%Y %X',
            canAlwaysGoUp: ['months', 'years'],
            ampm: true,
            onClose: function() {
                $scope.calculate_date_difference();
                $$('#total_amount').set('value', $scope.receipt.total_amount);
                $$('#balance').set('value', $scope.receipt.balance);
                },

        });
        
     }
    };
});
directives.directive('ngEnter', function() {
    return function(scope, element, attrs) {
        element.bind("keypress", function(event) {
            if(event.which === 13) {
                scope.$apply(function(){
                    scope.$eval(attrs.ngEnter);
                });
                event.preventDefault();
            }
        });
    };
});

directives.directive("fileread", [function () {
    return {
        scope: {
            fileread: "="
        },
        link: function (scope, element, attributes) {
            element.bind("change", function (changeEvent) {
                scope.$apply(function () {
                    scope.fileread = changeEvent.target.files[0];
                    // or all selected files:
                    // scope.fileread = changeEvent.target.files;
                });
            });
        }
    }
}]);