
from django.urls import re_path

from . import views

urlpatterns = [
    re_path('^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCode.as_view()),
    re_path('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.MsgCodeView.as_view()),
]
