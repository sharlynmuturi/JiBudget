from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import reverse_lazy

urlpatterns = [

    path('signup/', views.signup_view, name='signup'),
    path('', views.my_dashboard, name='my_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/', views.custom_report, name='custom_report'),
    path('custom-report/export/', views.export_report_excel, name='export_report_excel'),


    path('spending-power/', views.spending_power, name='spending_power'),

    path('top-up-savings/', views.top_up_savings, name='top_up_savings'),

    path('starting-balance/', views.add_starting_balance, name='add_starting_balance'),
    path('starting-budget/', views.add_starting_budget, name='add_starting_budget'),

    path("wallets/transfer/", views.add_wallet_transfer, name="add_wallet_transfer"),

    path('incomes/', views.income_list, name='income_list'),
    path('income/add/', views.add_income, name='add_income'),
    path('income/<int:income_id>/edit/', views.edit_income, name='edit_income'),
    path('income/<int:income_id>/delete/', views.delete_income, name='delete_income'),
    path('add-income-subcategory/', views.add_income_subcategory, name='add_income_subcategory'),

    path('expenses/', views.expense_list, name='expense_list'),
    path('expense/add/', views.add_expense, name='add_expense'),
    path('expense/<int:expense_id>/edit/', views.edit_expense, name='edit_expense'),
    path('expense/<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
    path('add-subcategory/', views.add_subcategory, name='add_subcategory'),

    path('expenses/add-source/', views.add_expense_source, name='add_expense_source'), # this is for both expenses and incomes

    path('savings/', views.saving_list, name='saving_list'),
    path('goal/add/', views.create_goal, name='create_goal'),
    path('goal/<int:goal_id>/edit/', views.edit_goal, name='edit_goal'),
    path('goal/<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),
    path('category/add/', views.add_category, name='add_category'),
    path('add-savings-subcategory/', views.add_savings_subcategory, name='add_savings_subcategory'),
    path('goal/<int:goal_id>/contribute/', views.add_to_goal, name='add_to_goal'),

    path('budgets/', views.all_budgets_view, name='all_budgets'),
    path('set-budget/', views.set_budget, name='set_budget'),
    path('set-budget/<int:pk>/', views.set_budget, name='edit_budget'),
    path('set-budget/delete/<int:pk>/', views.delete_budget, name='delete_budget'),
    path('budget-summary/', views.budget_vs_actual_view, name='budget_vs_actual'),
    path('budget-vs-actual/all/', views.all_budget_vs_actual_view, name='all_budget_vs_actual'),
    
    path('contact/', views.contact_view, name='contact'),

    path('wallets/', views.wallet_overview, name='wallet_overview'),

    path('onboarding/', views.onboarding_view, name='onboarding_view'),


    path("incomes/delete-selected/", views.delete_selected_incomes, name="delete_selected_incomes"),
    path("expenses/delete-selected/", views.delete_selected_expenses, name="delete_selected_expenses"),

    path('income/<int:income_id>/favourite/', views.toggle_favourite_income, name='toggle_favourite_income'),
    path('income/<int:income_id>/duplicate/', views.duplicate_income, name='duplicate_income'),

    path('expense/<int:expense_id>/favourite/', views.toggle_favourite_expense, name='toggle_favourite_expense'),
    path('expense/<int:expense_id>/duplicate/', views.duplicate_expense, name='duplicate_expense'),


    path('budget/<int:budget_id>/toggle-favourite/', views.toggle_favourite_budget, name='toggle_favourite_budget'),
    path('budget/<int:budget_id>/duplicate/', views.duplicate_budget, name='duplicate_budget'),

    path('manage-subcategories/', views.manage_subcategories, name='manage_subcategories'),
    path('manage-wallets/', views.manage_wallets, name='manage_wallets'),



    path('add/', views.add_investment_account, name='add_investment_account'),
    path('portfolio_dashboard/', views.portfolio_dashboard, name='portfolio_dashboard'),
    path('update_prices/', views.update_prices_view, name='update_prices'),
    path("accounts/<int:account_id>/add-transaction/", views.add_transaction, name="add_investment_transaction"),
    path('accounts/<int:account_id>/delete/', views.delete_investment_account, name='delete_investment_account'),
    path("investment/update/<int:account_id>/", views.update_investment_account, name="update_investment_account"),


    path('loans/', views.loan_list, name='loan_list'),
    path('loans/create/', views.create_loan, name='create_loan'),
    path('loans/<int:loan_id>/', views.loan_detail, name='loan_detail'),
    path('loans/<int:loan_id>/add-payment/', views.add_loan_payment, name='add_loan_payment'),
    path('loans/<int:pk>/delete/', views.loan_delete, name='loan_delete'),


    path('account/', views.account_settings, name='account'),
    path('update-profile/', views.update_profile, name='update_profile'),
    
    path('account/password/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        success_url=reverse_lazy('password_change_done')  # This is key!
    ), name='password_change'),
    
    path('account/password/success/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
      
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete')

]
