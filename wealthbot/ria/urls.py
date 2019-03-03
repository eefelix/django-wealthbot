from django.urls import path, re_path

from . import views

urlpatterns = [
    path('ria/change-profile', views.changeProfileIndex, name='rx_ria_change_profile'),
    path('ria/change-profile/profile', views.profile, name='rx_ria_profile'),
    path('ria/company-profile', views.companyProfile, name='rx_ria_company_profile'),
    path('ria/dashboard', views.index, name='rx_ria_dashboard'),
    path('ria/dashboard/billing', views.billingIndex, name='rx_ria_billing'),
    path('ria/dashboard/clients', views.clientsList, name='rx_ria_dashboard_clients'),
    path('ria/dashboard/clients/<str:tab>', views.clientsList, name='rx_ria_dashboard_clients'),
    path('ria/dashboard/client/<int:client_id>', views.showClient, name='rx_ria_dashboard_show_client'),
    path('ria/dashboard/clients-search', views.clientsSearch, name='rx_ria_dashboard_clients_search'),
    path('ria/dashboard/clients-with-prospects-search', views.clientsSearchWithProspects, name='rx_ria_dashboard_clients_with_prospects_search'),
    path('ria/dashboard/models/tab/<str:tab>', views.securities, name='rx_ria_dashboard_models_tab'),
    path('ria/dashboard/models', views.modelsIndex, name='rx_ria_models'),
    path('ria/dashboard/prospect/<int:client_id>/account/create', views.createClientAccount, name='rx_ria_prospect_create_client_account'),
    path('ria/dashboard/prospect/<int:client_id>/account/<int:account_id>/edit', views.editClientAccount, name='rx_ria_prospect_edit_client_account'),
    path('ria/dashboard/prospect/<int:client_id>/account/update-form', views.updateClientAccountForm, name='rx_ria_prospect_update_client_account_form'),
    path('ria/dashboard/prospect/<int:client_id>/account/update-owners-form', views.updateClientAccountOwnersForm, name='rx_ria_prospect_update_client_account_owners_form'),
    path('ria/dashboard/prospect/<int:client_id>/account/<int:account_id>/delete', views.deleteClientAccount, name='rx_ria_prospect_delete_client_account'),
    path('ria/dashboard/prospect/<int:client_id>/suggested-portfolio', views.suggestedPortfolio, { 'client_view': 0 }, name='rx_ria_prospect_portfolio'),
    path('ria/dashboard/prospect/<int:client_id>/suggested-portfolio/client-view', views.suggestedPortfolio, { 'client_view': 1 }, name='rx_ria_prospect_portfolio_client_view'),
    path('ria/dashboard/prospects', views.prospectIndex, name='rx_ria_prospects'),
    re_path(r'^ria/dashboard/prospects/(?P<order>.+?)/(?P<sort>.+?)/?$', views.prospectIndex, name='rx_ria_prospects'),
    path('ria/dashboard/prospects/delete', views.deleteProspect, name='rx_ria_prospects_delete'),
    path('ria/dashboard/prospects/invite', views.inviteProspect, name='rx_ria_prospects_invite'),
    path('ria/dashboard/rebalancing', views.rebalancing, name='rx_ria_dashboard_rebalancing'),
    path('ria/dashboard/risks', views.riskIndex, name='rx_ria_risk_profiling'),
    path('ria/dashboard/risks/test/result', views.testResult, name='rx_ria_risks_test_result'),
    path('ria/dashboard/swap-boxes', views.swapBoxes, name='rx_ria_dashboard_swap_boxes'),
    path('ria/dashboard/workflow', views.workflowIndex, name='rx_ria_workflow'),
    path('ria/dashboard/workflow/<str:tab>', views.workflowIndex, name='rx_ria_workflow_tab'),
    path('ria/dashboard/workflow/activity-summary/<int:id>/delete', views.deleteActivitySummary, name='rx_ria_workflow_activity_summary_delete'),
    path('ria/login-as/<str:username>', views.loginAs, name='rx_ria_login_as_client'),
    path('ria/user-management', views.userIndex, name='rx_ria_user_management'),
]
