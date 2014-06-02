from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from web.views import *

urlpatterns = patterns('',
	url(r'^$', Home.as_view(), name='home'),
	url(r'login/$', Login.as_view(), name='login'),
	url(r'logout/$', login_required(Logout.as_view()), name='logout'),
	url(r'add_client/$', login_required(AddClient.as_view()), name='add_client'),
	url(r'clients/$', login_required(ClientList.as_view()), name='clients'),
)