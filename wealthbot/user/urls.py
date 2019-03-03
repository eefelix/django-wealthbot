from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as user_views
from . import forms as user_forms

urlpatterns = [
    path('', user_views.index, name='rx_user_homepage'),
    path('ria/registration', user_views.ria_registration, name='rx_ria_register'),
    path('client/registration/<int:ria_id>', user_views.registration, name='rx_client_registration'),
    path('file/logo/ria/<int:ria_id>', user_views.logo, name='rx_file_download'),
    path('login', auth_views.LoginView.as_view(template_name='user/security_login.html', authentication_form=user_forms.LoginForm), name='fos_user_security_login'),
    path('after-login', user_views.afterLogin, name='rx_after_login'),
    path('logout', auth_views.LogoutView.as_view(template_name='user/default_index.html'), name='fos_user_security_logout'),
]
