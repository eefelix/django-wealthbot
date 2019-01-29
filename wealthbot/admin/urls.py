from django.urls import path

from . import views

urlpatterns = [
    path('admin', views.dashboardIndex, name='rx_admin_homepage'),
]
