
from django.urls import re_path

from users import views

urlpatterns = [
    re_path('^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UserName.as_view()),
    re_path('^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.Mobile.as_view()),
]
