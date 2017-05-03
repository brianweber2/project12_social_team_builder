from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'new/$', views.CreateProjectView.as_view(), name='new_project'),
]
