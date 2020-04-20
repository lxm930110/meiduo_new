
from django.urls import re_path

from . import views

urlpatterns = [
    re_path('^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCode.as_view()),
]
