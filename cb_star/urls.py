from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^(\d+)/$',views.star),
    re_path(r'^add(\d+)/$',views.add),
    re_path(r'^delete(\d+)/$',views.delete),
    re_path(r'^add_cart(\d+)_(\d+)/$',views.add_cart),
]