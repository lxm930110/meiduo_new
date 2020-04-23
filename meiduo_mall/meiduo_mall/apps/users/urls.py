
from django.urls import re_path

from users import views

urlpatterns = [
    re_path('^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UserNameView.as_view()),
    re_path('^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileView.as_view()),
    re_path('^register/$', views.RegisterUserView.as_view()),
    re_path('^login/$', views.LoginView.as_view()),
    re_path('^logout/$', views.LogoutView.as_view()),
    re_path('^info/$', views.UserCenterInfoView.as_view()),
]
