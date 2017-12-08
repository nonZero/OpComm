from django.urls import path

from meetings import views

urlpatterns = [

    path('', views.MeetingList.as_view(), name="history"),

    path('<int:id>/', views.MeetingDetailView.as_view(), name="meeting"),
    path('<int:id>/protocol/', views.MeetingProtocolView.as_view(),
         name="meeting_protocol"),
]
