from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from web.views import *

urlpatterns = patterns('',
	url(r'^$', Home.as_view(), name='home'),
	url(r'^login/$', Login.as_view(), name='login'),
	url(r'^logout/$', login_required(Logout.as_view()), name='logout'),
	url(r'^add_vehicle/$', login_required(AddVehicle.as_view()), name='add_vehicle'),
	url(r'^vehicles/$', login_required(VehicleList.as_view()), name='vehicles'),
	url(r'^add_vehicle_type/$', login_required(AddVehicleType.as_view()), name='add_vehicle_type'),
	url(r'^vehicle_type/list/$', login_required(VehicleTypeList.as_view()), name='vehicle_types'),
	url(r'^edit_vehicle/(?P<vehicle_id>\d+)/$', login_required(EditVehicle.as_view()), name='edit_vehicle'),
	url(r'^print_rent_agreement/$', login_required(PrintRentAgreement.as_view()), name='print_rent_agreement'),
	url(r'^rent_agreement/$', login_required(RentAgreementView.as_view()), name='rent_agreement'),
	url(r'^receive_car/$', login_required(ReceiveCarView.as_view()), name='receive_car'),
	url(r'^agreements/$', login_required(AgreementDetails.as_view()), name='agreements'),
	
	url(r'^drivers/$', login_required(DriversList.as_view()), name='drivers'),
	url(r'^add_driver/$', login_required(AddDriver.as_view()), name='add_driver'),
	url(r'^print_receipt/$', login_required(PrintReceiptCar.as_view()), name='print_receipt'),

	url(r'^rent_agreement_details/$', login_required(RentAgreementDetails.as_view()), name='rent_agreement_details'),
	url(r'^case_entry/$', login_required(CaseEntry.as_view()), name='case_entry'),
	url(r'^case_types/$', login_required(TypeOfCaseList.as_view()), name='case_types'),
	url(r'^add_case_type/$', login_required(AddTypeOfCase.as_view()), name='add_case_type'),
)