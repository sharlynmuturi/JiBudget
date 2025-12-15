# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ExpenseViewSet, ExpenseCategoryViewSet, ExpenseSubCategoryViewSet,
    IncomeViewSet, IncomeCategoryViewSet, IncomeSubCategoryViewSet,
    ExpenseSourceViewSet, SavingsGoalViewSet, BudgetItemViewSet,
    LoanAccountViewSet, LoanPaymentViewSet,
    InvestmentAccountViewSet, InvestmentTransactionViewSet,
    WalletTransferViewSet
)

router = DefaultRouter()
router.register('expenses', ExpenseViewSet, basename='expenses')
router.register('incomes', IncomeViewSet, basename='incomes')
router.register('expense-categories', ExpenseCategoryViewSet, basename='expense-categories')
router.register('expense-subcategories', ExpenseSubCategoryViewSet, basename='expense-subcategories')
router.register('income-categories', IncomeCategoryViewSet, basename='income-categories')
router.register('income-subcategories', IncomeSubCategoryViewSet, basename='income-subcategories')
router.register('sources', ExpenseSourceViewSet, basename='sources')
router.register('savings-goals', SavingsGoalViewSet, basename='savings-goals')
router.register('budgets', BudgetItemViewSet, basename='budgets')
router.register('loan-accounts', LoanAccountViewSet, basename='loan-accounts')
router.register('loan-payments', LoanPaymentViewSet, basename='loan-payments')
router.register('investment-accounts', InvestmentAccountViewSet, basename='investment-accounts')
router.register('investment-transactions', InvestmentTransactionViewSet, basename='investment-transactions')
router.register('wallet-transfers', WalletTransferViewSet, basename='wallet-transfers')

urlpatterns = [
    path('', include(router.urls)),

    # 🔐 JWT Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
