# api/serializers.py
from rest_framework import serializers
from budget.models import (
    ExpenseSource, IncomeCategory, IncomeSubCategory, Income,
    ExpenseCategory, ExpenseSubCategory, Expense,
    SavingsGoal, BudgetItem, LoanAccount, LoanPayment,
    InvestmentAccount, InvestmentTransaction,
    WalletTransfer
)

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'user', 'category', 'category_name', 'subcategory',
            'subcategory_name', 'description', 'amount', 'source', 'source_name',
            'date', 'is_favourite'
        ]

class IncomeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    income_source_name = serializers.CharField(source='income_source.name', read_only=True)

    class Meta:
        model = Income
        fields = [
            'id', 'user', 'category', 'category_name', 'subcategory',
            'subcategory_name', 'income_source', 'income_source_name',
            'source', 'amount', 'date', 'is_favourite'
        ]

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'is_savings_generated', 'is_loan_generated', 'is_investment_generated']

class ExpenseSubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = ExpenseSubCategory
        fields = ['id', 'category', 'category_name', 'name']

class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['id', 'name']

class IncomeSubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = IncomeSubCategory
        fields = ['id', 'category', 'category_name', 'name']

class ExpenseSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSource
        fields = ['id', 'name']

class SavingsGoalSerializer(serializers.ModelSerializer):
    wallet_name = serializers.CharField(source='wallet.name', read_only=True)

    class Meta:
        model = SavingsGoal
        fields = ['id', 'user', 'name', 'target_amount', 'current_amount', 'wallet', 'wallet_name', 'created_at', 'updated_at']


class BudgetItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = BudgetItem
        fields = ['id', 'user', 'category', 'category_name', 'amount', 'month', 'year']


class LoanAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanAccount
        fields = '__all__'


class LoanPaymentSerializer(serializers.ModelSerializer):
    loan_name = serializers.CharField(source='loan.name', read_only=True)

    class Meta:
        model = LoanPayment
        fields = ['id', 'loan', 'loan_name', 'amount', 'date', 'source']


class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = '__all__'


class InvestmentTransactionSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source='account.name', read_only=True)

    class Meta:
        model = InvestmentTransaction
        fields = ['id', 'account', 'account_name', 'action', 'units', 'price_per_unit', 'amount', 'wallet', 'date']


class WalletTransferSerializer(serializers.ModelSerializer):
    from_wallet_name = serializers.CharField(source='from_wallet.name', read_only=True)
    to_wallet_name = serializers.CharField(source='to_wallet.name', read_only=True)

    class Meta:
        model = WalletTransfer
        fields = ['id', 'user', 'from_wallet', 'from_wallet_name', 'to_wallet', 'to_wallet_name', 'amount', 'date']
