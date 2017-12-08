from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include, reverse_lazy, re_path
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog

import users
from meetings.views import MeetingCreateView
from . import views
from users.forms import OCPasswordResetForm, OCPasswordResetConfirmForm
from users.models import CODE_LENGTH
from users.views import AcceptInvitationView
import communities.views

urlpatterns = [
                  path('', communities.views.LandingPage.as_view(), name='landing'),
                  path('communities/', communities.views.CommunityList.as_view(), name='home'),
                  path('about/', communities.views.About.as_view(), name='about'),
                  path('<int:id>/', include('communities.urls')),
                  path('<int:community_id>/upcoming/close/',
                       MeetingCreateView.as_view(),
                       name="upcoming_close"),
                  path('<int:community_id>/members/', include('users.urls')),
                  path('<int:community_id>/issues/', include('issues.urls')),
                  path('<int:community_id>/history/', include('meetings.urls')),
                  path('login/', views.login_user, {
                      'template_name': 'login.html'},
                       name="login"),
                  path('logout/', LogoutView.as_view(),
                       {'next_page': reverse_lazy('home')}, name="logout"),
                  re_path('invitation/(?P<code>[a-z0-9]{%d})/' % CODE_LENGTH,
                       AcceptInvitationView.as_view(),
                       name="accept_invitation"),
                  path('user/password/reset/',
                       users.views.oc_password_reset,
                       {'post_reset_redirect': '/user/password/reset/done/',
                        'password_reset_form': OCPasswordResetForm},
                       name="password_reset"),
                  path('user/password/reset/done/',
                       PasswordResetDoneView.as_view()),
                  path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
                       {'post_reset_redirect': '/user/password/done/',
                        'set_password_form': OCPasswordResetConfirmForm}),
                  path('user/password/done/', PasswordResetCompleteView.as_view()),
                  path('admin/', admin.site.urls),
                  path('django-rq/', include('django_rq.urls')),
                  path('jsi18n/', JavaScriptCatalog.as_view(packages=['issues', 'communities']), 'jsi18n'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
