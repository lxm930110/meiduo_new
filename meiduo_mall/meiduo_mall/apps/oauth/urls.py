
from django.urls import re_path

from . import views

urlpatterns = [
    re_path('^qq/authorization/$', views.QQURLView.as_view()),
    re_path('^oauth_callback/$', views.QQLoginView.as_view()),

]
