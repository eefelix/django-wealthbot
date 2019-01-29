from django.urls import path

from . import views

urlpatterns = [
    path('ria/company-profile', views.companyProfile, name='rx_ria_company_profile'),
    path('ria/dashboard/risks/test/result', views.testResult, name='rx_ria_risks_test_result'),
    path('ria/dashboard/prospect/<int:client_id>/account/<int:account_id>/edit', views.editClientAccount, name='rx_ria_prospect_edit_client_account'),
    path('ria/dashboard/prospect/<int:client_id>/account/<int:account_id>/delete', views.deleteClientAccount, name='rx_ria_prospect_delete_client_account'),
]
