from django.urls import path

from users import views

urlpatterns = [
    path(r'^$', views.MembershipList.as_view(), name="members"),
    path(r'^(?P<pk>\d+)/$', views.MemberProfile.as_view(), name="member_profile"),
    path(r'^(?P<pk>\d+)/delete-invitation/$', views.DeleteInvitationView.as_view(),
         name="delete_invitation"),
    path(r'^autocomp/$', views.AutocompleteMemberName.as_view(), name="ac_user"),
    path(r'^import/$', views.ImportInvitationsView.as_view(), name="import_invitations"),
]
