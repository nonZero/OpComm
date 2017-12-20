from django.urls import path

from communities import views

urlpatterns = [
    path('', views.UpcomingMeetingView.as_view(), name='community'),
    path('upcoming/publish/', views.PublishUpcomingView.as_view(), name="upcoming_publish"),
    path('upcoming/start/', views.StartMeetingView.as_view(), name="upcoming_start"),
    path('upcoming/end/', views.EndMeetingView.as_view(), name="upcoming_end"),
    path('edit-summary/', views.EditUpcomingSummaryView.as_view(), name="upcoming_edit_summary"),
    path('upcoming/publish/preview/', views.PublishUpcomingMeetingPreviewView.as_view(),
         name='preview_upcoming_meeting'),
    path('upcoming/edit/', views.EditUpcomingMeetingView.as_view(), name="upcoming_edit"),
    path('upcoming/participants/', views.EditUpcomingMeetingParticipantsView.as_view(),
         name="upcoming_edit_participants"),
    path('upcoming/participants/delete-participant/<int:participant_id>/', views.DeleteParticipantView.as_view(),
         name="delete_participant"),
    path('protocol-preview/', views.ProtocolDraftPreviewView.as_view(), name='preview_ongoing_protocol'),
    path('search/', views.CommunitySearchView.as_view(), name='community_search'),

    # FOR TESTING ONLY!
    path('upcoming/sum_votes/', views.SumVotesView.as_view(), name="sum_votes"),
]
