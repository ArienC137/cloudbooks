from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^$',views.cart),
    re_path(r'^add(\d+)_(\d+)/$',views.add),
    re_path(r'^edit(\d+)_(\d+)/$',views.edit),
    re_path(r'^delete(\d+)/$',views.delete),
]