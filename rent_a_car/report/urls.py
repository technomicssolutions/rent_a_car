from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from report.views import *

urlpatterns = patterns('',
    url(r'^rent_report/$', RentReport.as_view(), name='rent_report'),
)