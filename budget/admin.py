from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Income, Expense, ExpenseCategory, ExpenseSubCategory, SavingsGoal, BudgetItem, IncomeCategory, IncomeSubCategory,ExpenseSource, LoanAccount, LoanPayment
from .models import InvestmentAccount, InvestmentTransaction, PriceHistory

from .models import WalletTransfer

from .models import UserHiddenSubCategory, UserHiddenIncomeSubCategory, UserHiddenWallet


admin.site.register(Income)
admin.site.register(IncomeCategory)
admin.site.register(IncomeSubCategory)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseSubCategory)
admin.site.register(ExpenseSource)
admin.site.register(SavingsGoal)
admin.site.register(BudgetItem)

admin.site.register(LoanAccount)
admin.site.register(LoanPayment)

admin.site.register(InvestmentAccount)
admin.site.register(InvestmentTransaction)
admin.site.register(PriceHistory)

admin.site.register(WalletTransfer)

admin.site.register(UserHiddenSubCategory)
admin.site.register(UserHiddenIncomeSubCategory)
admin.site.register(UserHiddenWallet)
