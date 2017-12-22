from django.urls import path

from users import views

urlpatterns = [
    path('', views.MembershipList.as_view(), name="members"),
    path('<int:pk>/', views.MemberProfile.as_view(), name="member_profile"),
    path('<int:pk>/delete-invitation/', views.DeleteInvitationView.as_view(),
         name="delete_invitation"),
    path('autocomp/', views.AutocompleteMemberName.as_view(), name="ac_user"),
    path('import/', views.ImportInvitationsView.as_view(), name="import_invitations"),
]
