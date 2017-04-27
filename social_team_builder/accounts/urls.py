from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'signin/$', views.SignInView.as_view(), name='signin'),
    url(r'signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_]+)$',
        views.UserProfileView.as_view(),
        name='profile'),
    url(r'^update/profile/(?P<username>[a-zA-Z0-9_]+)$',
        views.UserProfileUpdateView.as_view(),
        name='update_profile'),
]
