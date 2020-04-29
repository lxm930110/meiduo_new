
from django.urls import re_path

from users import views

urlpatterns = [
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UserNameView.as_view()),
    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileView.as_view()),
    re_path(r'^register/$', views.RegisterUserView.as_view()),
    re_path(r'^login/$', views.LoginView.as_view()),
    re_path(r'^logout/$', views.LogoutView.as_view()),
    re_path(r'^info/$', views.UserCenterInfoView.as_view()),
    re_path(r'^emails/$', views.EmailView.as_view()),
    re_path(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    re_path(r'^addresses/create/$', views.CreateAddressView.as_view()),
    re_path(r'^addresses/$', views.ShowAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/$', views.UpdateAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    re_path(r'^password/$', views.ModifyPasswordView.as_view()),
]
