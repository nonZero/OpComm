from django.urls import path

from meetings import views

urlpatterns = [

    path(r'^$', views.MeetingList.as_view(), name="history"),

    path(r'^(?P<pk>\d+)/$', views.MeetingDetailView.as_view(), name="meeting"),
    path(r'^(?P<pk>\d+)/protocol/$', views.MeetingProtocolView.as_view(),
         name="meeting_protocol"),
]
