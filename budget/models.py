from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import datetime
from django.utils import timezone

from django.db import transaction


# Expense source is for both expenses and incomes
class ExpenseSource(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'user')
        ordering = ['name']


class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class IncomeSubCategory(models.Model):
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(IncomeSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    income_source = models.ForeignKey(ExpenseSource, on_delete=models.SET_NULL, null=True)

    source = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(null=True, default=datetime.date.today)
    is_favourite = models.BooleanField(default=False)

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    is_savings_generated = models.BooleanField(default=False)  # <-- Add this
    is_loan_generated = models.BooleanField(default=False)  # <-- Add this
    is_investment_generated = models.BooleanField(default=False)  # <-- Add this

    def __str__(self):
        return self.name


class ExpenseSubCategory(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(ExpenseSubCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.ForeignKey(ExpenseSource, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True, default=datetime.date.today)
    is_favourite = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if not is_new:
            return  # only trigger on create, not edits

        # --- 1️⃣ SAVINGS LINK ---
        if self.category and self.category.is_savings_generated:
            goal = SavingsGoal.objects.filter(
                user=self.user, subcategory=self.subcategory
            ).first()
            if goal:
                goal.saved_so_far += self.amount
                goal.save(update_fields=["saved_so_far"])

        # --- 2️⃣ LOAN LINK ---
        elif self.category and self.category.is_loan_generated:
            loan = LoanAccount.objects.filter(user=self.user, name=self.subcategory.name).first()
            if loan:
                LoanPayment.objects.create(
                    loan=loan,
                    amount=self.amount,
                    date=self.date,
                )

        # --- 3️⃣ INVESTMENT LINK ---
        elif self.category and self.category.is_investment_generated:
            account = InvestmentAccount.objects.filter(user=self.user, name=self.subcategory.name).first()
            if account:
                InvestmentTransaction.objects.create(
                    account=account,
                    wallet=self.source,
                    date=self.date,
                    action="DEPOSIT",
                    amount=self.amount,
                    is_investment_generated=True,
                )


class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(ExpenseSubCategory, on_delete=models.CASCADE, null=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    saved_so_far = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0'))
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def progress(self):
        if self.target_amount > 0:
            return (self.saved_so_far / self.target_amount) * 100
        return 0

    def __str__(self):
        return f"{self.subcategory.name} Goal"


class BudgetItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField(null=True, default=datetime.date.today)
    category = models.ForeignKey('ExpenseCategory', on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey('ExpenseSubCategory', on_delete=models.CASCADE, null=True, blank=True)
    forecasted_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_favourite = models.BooleanField(default=False)   # ⭐ NEW


    class Meta:
        unique_together = ('user', 'month', 'category', 'subcategory')

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')} Budget"

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import datetime

class LoanAccount(models.Model):
    FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('yearly', 'Yearly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    principal = models.DecimalField(max_digits=12, decimal_places=2)
    annual_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # e.g. 12.5%
    term_periods = models.PositiveIntegerField()
    payment_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='monthly')
    start_date = models.DateField(default=datetime.date.today)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def remaining_balance(self):
        total_paid = sum(payment.amount for payment in self.payments.all())
        return max(self.principal - total_paid, Decimal('0.00'))


class LoanPayment(models.Model):
    loan = models.ForeignKey(LoanAccount, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.date.today)
    is_extra_payment = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.loan.name} - {self.amount} on {self.date}"


# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.core.exceptions import ValidationError
import yfinance as yf
from django.db import models



class InvestmentAccount(models.Model):
    ASSET_TYPES = [
        ('stock', 'Stock / ETF'),
        ('crypto', 'Cryptocurrency'),
        ('bond', 'Bond'),
        ('mmf', 'Money Market Fund'),
        ('real_estate', 'Real Estate'),
        ('sacco', 'SACCO / CHAMA'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    symbol = models.CharField(max_length=50, blank=True, null=True)
    initial_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    units_held = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)  # For stocks/MMFs 

    # NEW FIELDS
    face_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # for bonds
    coupon_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # % for bonds
    yield_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)   # % for MMFs
    rental_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # real estate
    expenses = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # real estate

    income_so_far = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    expenses_so_far = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    # Bond-specific
    issue_date = models.DateField(blank=True, null=True)
    maturity_date = models.DateField(blank=True, null=True)
    is_callable = models.BooleanField(default=False)
    interest_frequency = models.CharField(max_length=20, blank=True, null=True)


    base_date = models.DateField(blank=True, null=True)


    # SACCO-specific fields
    sacco_capital_share = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sacco_minimum_contribution = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sacco_total_contributions = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    sacco_contribution_frequency = models.CharField(max_length=20, blank=True, null=True)
    sacco_dividend_frequency = models.CharField(max_length=20, blank=True, null=True)
    sacco_dividends_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)


    currency = models.CharField(max_length=10, default="KES")  # optional

    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        if self.symbol:
            try:
                import yfinance as yf
                ticker = yf.Ticker(self.symbol)
                hist = ticker.history(period="1d")
                if hist.empty:
                    raise ValidationError({'symbol': "Invalid symbol. Enter a valid ticker (e.g., AAPL, TSLA)."})
            except Exception:
                raise ValidationError({'symbol': "Could not validate symbol. Try again."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.asset_type})"


class InvestmentTransaction(models.Model):
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    wallet = models.ForeignKey("ExpenseSource", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()

    ACTION_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('DIVIDEND', 'Dividend'),   # Stocks/ETFs
        ('INTEREST', 'Interest'),   # Bonds/MMFs
        ('RENTAL', 'Rental Income'), # Real Estate
        ('EXPENSE', 'Expense'), # Real Estate
        ('DEPOSIT', 'Deposit'),        # MMFs/Real Estate Add Funds
        ('WITHDRAW', 'Withdraw'),      # MMFs/Real Estate Remove Funds
        ('CAPITAL_SHARE', 'Capital'),
        ('CONTRIBUTION', 'Contribution'),
    ]
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)

    # Core transaction details
    units = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)  # For stocks/MMFs
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # For stocks/MMFs
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    # Optional extra fields depending on asset type
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Bonds/MMFs
    maturity_date = models.DateField(null=True, blank=True)  # Bonds
    notes = models.TextField(blank=True, null=True)  # Freeform e.g. property location, fund details

    # ðŸ”— Links to budget system
    linked_expense = models.OneToOneField('Expense', on_delete=models.SET_NULL, null=True, blank=True)
    linked_income = models.OneToOneField('Income', on_delete=models.SET_NULL, null=True, blank=True)

    is_investment_generated = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.action} {self.account.name} on {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        user = self.account.user
        wallet = self.wallet

        # Define action mappings
        expense_actions = ["BUY", "DEPOSIT", "EXPENSE", "CAPITAL_SHARE", "CONTRIBUTION"]
        income_actions = ["SELL", "DIVIDEND", "INTEREST", "RENTAL", "WITHDRAW"]

        if self.action in expense_actions and not self.linked_expense:
            cat, _ = ExpenseCategory.objects.get_or_create(user=user, name="Investments")
            subcat, _ = ExpenseSubCategory.objects.get_or_create(user=user, category=cat, name=self.account.name)
            expense = Expense.objects.create(
                user=user,
                category=cat,
                subcategory=subcat,
                description=f"{self.action} - {self.account.name}",
                amount=self.amount,
                source=wallet,
                date=self.date,
            )
            self.linked_expense = expense
            self.is_investment_generated = True  

            super().save(update_fields=["linked_expense", "is_investment_generated"])

        elif self.action in income_actions and not self.linked_income:
            cat, _ = IncomeCategory.objects.get_or_create(user=user, name="Investment Income")
            subcat, _ = IncomeSubCategory.objects.get_or_create(user=user, category=cat, name=self.account.name)
            income = Income.objects.create(
                user=user,
                category=cat,
                subcategory=subcat,
                income_source=wallet,
                source=f"{self.action} from {self.account.name}",
                amount=self.amount,
                date=self.date,
            )
            self.linked_income = income
            super().save(update_fields=["linked_income"])

class PriceHistory(models.Model):
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.FloatField()
    currency = models.CharField(max_length=10, default="USD")  # new field

class WalletTransfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_wallet = models.ForeignKey(
        ExpenseSource, related_name="wallet_transfers_out", on_delete=models.CASCADE
    )
    to_wallet = models.ForeignKey(
        ExpenseSource, related_name="wallet_transfers_in", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.date.today)
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.amount} from {self.from_wallet} to {self.to_wallet}"


    def save(self, *args, **kwargs):
        if not self.pk:  # only on create
            with transaction.atomic():
                # Log as an Expense from "from_wallet"
                Expense.objects.create(
                    user=self.user,
                    category=None,
                    subcategory=None,
                    description=f"Transfer to {self.to_wallet.name}",
                    amount=self.amount,
                    source=self.from_wallet,
                    date=self.date,
                )
                # Log as an Income to "to_wallet"
                Income.objects.create(
                    user=self.user,
                    category=None,
                    subcategory=None,
                    source=f"Transfer from {self.from_wallet.name}",
                    amount=self.amount,
                    income_source=self.to_wallet,
                    date=self.date,
                )
        super().save(*args, **kwargs)

class UserHiddenSubCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(ExpenseSubCategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'subcategory')

    def __str__(self):
        return f"{self.user.username} hides {self.subcategory.name}"


class UserHiddenIncomeSubCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subcategory = models.ForeignKey('IncomeSubCategory', on_delete=models.CASCADE)
    hidden = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'subcategory')

    def __str__(self):
        return f"{self.user.username} - {self.subcategory.name}"

class UserHiddenWallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(ExpenseSource, on_delete=models.CASCADE)
    hidden = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'wallet')

    def __str__(self):
        return f"{self.user.username} - {self.wallet.name}"
