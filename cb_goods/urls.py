from django.urls import path,re_path
from . import views
from .views import *

urlpatterns = [
    re_path(r'^list(\d+)_(\d+)_(\d+)/$',views.list),
    re_path(r'^(\d+)/$',views.detail),
    re_path(r'^classify(\d+)_(\d+)_(\d+)/$',views.classify),
    re_path(r'^search/$',MySearchView()),
]
