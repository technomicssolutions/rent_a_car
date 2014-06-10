from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from report.views import *

urlpatterns = patterns('',
    url(r'^rent_report/$', login_required(RentReport.as_view()), name='rent_report'),
    url(r'^vehicle_report/$', login_required(VehicleReport.as_view()), name='vehicle_report'),
    url(r'^outstanding_vehicle_report/$', login_required(VehicleOutstandingReport.as_view()), name='outstanding_vehicle_report'),
)