from django.conf.urls import url
from app import views

urlpatterns = [
	url(r'^machine/$', views.MachineListView.as_view()),
	url(r'^machine/(?P<pk>[0-9]+)/$', views.MachineDetailView.as_view()),

	url(r'^machine/(?P<pk>[0-9]+)/periodic/$', views.MachinePeriodicView.as_view()),

	url(r'^cinmanuser/$', views.CINManUserListView.as_view()),
	url(r'^cinmanuser/(?P<pk>[0-9]+)/$', views.CINManUserDetailView.as_view()),

	url(r'^machineloginsession/$', views.MachineLoginSessionListView.as_view()),
	url(r'^machineloginsession/(?P<pk>[0-9]+)/$', views.MachineLoginSessionDetailView.as_view()),

	url(r'^machineuser/$', views.MachineUserListView.as_view()),
	url(r'^machineuser/(?P<pk>[0-9]+)/$', views.MachineUserDetailView.as_view()),

	url(r'^logentry/$', views.LogEntryListView.as_view()),
	url(r'^logentry/(?P<pk>[0-9]+)/$', views.LogEntryDetailView.as_view()),
]
