from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from web.views import *

urlpatterns = patterns('',
	url(r'^$', Home.as_view(), name='home'),
	url(r'login/$', Login.as_view(), name='login'),
	url(r'logout/$', login_required(Logout.as_view()), name='logout'),
	url(r'add_client/$', login_required(AddClient.as_view()), name='add_client'),
	url(r'edit_client/(?P<client_id>\d+)/$', login_required(EditClient.as_view()), name='edit_client'),
	url(r'clients/$', login_required(ClientList.as_view()), name='clients'),
	url(r'add_vehicle/$', login_required(AddVehicle.as_view()), name='add_vehicle'),
	url(r'vehicles/$', login_required(Vehicles.as_view()), name='vehicles'),
	url(r'add_vehicle_type/$', login_required(AddVehicleType.as_view()), name='add_vehicle_type'),
	url(r'vehicle_type/list/$', login_required(VehicleTypeList.as_view()), name='vehicle_types'),
	url(r'edit_vehicle/(?P<vehicle_id>\d+)/$', login_required(EditVehicle.as_view()), name='edit_vehicle')
)