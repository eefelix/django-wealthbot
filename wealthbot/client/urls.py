from django.urls import path

from . import views

urlpatterns = [
    path('client/profile/step-one', views.stepOne, name='rx_client_profile_step_one'),
    path('client/profile/step-two', views.stepTwo, name='rx_client_profile_step_two'),
    path('client/profile/step-three', views.stepThree, name='rx_client_profile_step_three'),
    path('client/profile/step-three-back', views.stepThreeBack, name='rx_client_step_three_back'),
    path('client/profile/step-three-complete', views.completeStepThree, name='rx_client_profile_step_three_complete'),
    path('client/profile/check-accounts-sum', views.checkAccountsSum, name='rx_client_profile_check_accounts_sum'),
    path('client/profile/show-accounts-table', views.showAccountsTable, name='rx_client_profile_show_accounts_table'),
    path('client/profile/show-success-message', views.showSuccessMessage, name='rx_client_profile_show_success_message'),
    path('client/profile/show-deposit-account-form', views.showDepositAccountForm, name='rx_client_profile_show_deposit_account_form'),
    path('client/profile/create-account/<str:group>', views.createAccount, name='rx_client_profile_create_account'),
    path('client/profile/update-account-form/<str:group>', views.updateAccountForm, name='rx_client_profile_update_account_form'),
    path('client/profile/account/<int:id>/edit', views.editAccount, name='rx_client_edit_account'),
    path('client/profile/account/<int:id>/delete', views.deleteAccount, name='rx_client_delete_account'),
    path('client/portfolio', views.index, name='rx_client_portfolio'),
    path('client/portfolio/final/accept', views.acceptPortfolio, name='rx_client_accept_final_portfolio'),
    path('client/portfolio/account/<int:account_id>/consolidated-accounts', views.consolidatedAccounts, name='rx_client_portfolio_consolidated_accounts'),
    path('client/portfolio/account/<int:account_id>/funds', views.outsideFunds, name='rx_client_portfolio_outside_funds'),
    path('client/dashboard/account-management', views.accountManagement, name='rx_client_dashboard_account_management'),
    path('client/dashboard/transfer/account/<int:account_id>/select_system_account', views.selectSystemAccount, name='rx_client_dashboard_select_system_account'),
    path('client/transfer/account/<int:account_id>', views.account, name='rx_client_transfer_account'),
]
