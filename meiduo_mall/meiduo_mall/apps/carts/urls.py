
from django.urls import re_path

from . import views

urlpatterns = [
        re_path(r'^carts/$', views.AddCarts.as_view()),
]
