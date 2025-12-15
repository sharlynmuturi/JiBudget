from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from budget.models import (
    Expense, ExpenseCategory, ExpenseSubCategory,
    Income, IncomeCategory, IncomeSubCategory,
    ExpenseSource, SavingsGoal, BudgetItem,
    LoanAccount, LoanPayment,
    InvestmentAccount, InvestmentTransaction,
    WalletTransfer
)
from .serializers import (
    ExpenseSerializer, ExpenseCategorySerializer, ExpenseSubCategorySerializer,
    IncomeSerializer, IncomeCategorySerializer, IncomeSubCategorySerializer,
    ExpenseSourceSerializer, SavingsGoalSerializer, BudgetItemSerializer,
    LoanAccountSerializer, LoanPaymentSerializer,
    InvestmentAccountSerializer, InvestmentTransactionSerializer,
    WalletTransferSerializer
)


# ---------- EXPENSES ----------
class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- INCOMES ----------
class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- CATEGORIES ----------
class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseCategory.objects.filter(user=self.request.user) | ExpenseCategory.objects.filter(user__isnull=True)


class ExpenseSubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSubCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseSubCategory.objects.filter(user=self.request.user) | ExpenseSubCategory.objects.filter(user__isnull=True)


class IncomeCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncomeCategory.objects.filter(user=self.request.user) | IncomeCategory.objects.filter(user__isnull=True)


class IncomeSubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSubCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return IncomeSubCategory.objects.filter(user=self.request.user) | IncomeSubCategory.objects.filter(user__isnull=True)


# ---------- SOURCES (WALLETS) ----------
class ExpenseSourceViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpenseSource.objects.filter(user=self.request.user) | ExpenseSource.objects.filter(user__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- SAVINGS ----------
class SavingsGoalViewSet(viewsets.ModelViewSet):
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- BUDGET ----------
class BudgetItemViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BudgetItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ---------- LOANS ----------
class LoanAccountViewSet(viewsets.ModelViewSet):
    serializer_class = LoanAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoanAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LoanPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = LoanPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoanPayment.objects.filter(loan__user=self.request.user)


# ---------- INVESTMENTS ----------
class InvestmentAccountViewSet(viewsets.ModelViewSet):
    serializer_class = InvestmentAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InvestmentAccount.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvestmentTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = InvestmentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InvestmentTransaction.objects.filter(account__user=self.request.user)


# ---------- WALLET TRANSFERS ----------
class WalletTransferViewSet(viewsets.ModelViewSet):
    serializer_class = WalletTransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WalletTransfer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
