from django.urls import path

from communities import views

urlpatterns = [
    path(r'^$', views.UpcomingMeetingView.as_view(), name='community'),
    path(r'^upcoming/publish/$', views.PublishUpcomingView.as_view(),
         name="upcoming_publish"),
    path(r'^upcoming/start/$', views.StartMeetingView.as_view(),
         name="upcoming_start"),
    path(r'^upcoming/end/$', views.EndMeetingView.as_view(),
         name="upcoming_end"),
    path(r'^edit-summary/$', views.EditUpcomingSummaryView.as_view(),
         name="upcoming_edit_summary"),
    path(r'^upcoming/publish/preview/$',
         views.PublishUpcomingMeetingPreviewView.as_view(),
         name='preview_upcoming_meeting'),
    path(r'^upcoming/edit/$', views.EditUpcomingMeetingView.as_view(),
         name="upcoming_edit"),
    path(r'^upcoming/participants/$',
         views.EditUpcomingMeetingParticipantsView.as_view(),
         name="upcoming_edit_participants"),
    path(r'^upcoming/participants/delete-participant/(?P<participant_id>\d+)/$', views.DeleteParticipantView.as_view(),
         name="delete_participant"),
    # FOR TESTING ONLY!
    path(r'^upcoming/sum_votes/$', views.SumVotesView.as_view(), name="sum_votes"),
    path(r'^protocol-preview/$',
         views.ProtocolDraftPreviewView.as_view(),
         name='preview_ongoing_protocol'),
    path(r'^search/$', views.CommunitySearchView.as_view(), name='community_search'),
]
