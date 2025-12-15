from django import forms
from .models import Income, Expense, ExpenseCategory, ExpenseSubCategory, SavingsGoal, BudgetItem, IncomeCategory, IncomeSubCategory, ExpenseSource, WalletTransfer
from django.db import models
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserHiddenWallet, UserHiddenSubCategory, UserHiddenIncomeSubCategory

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['subcategory', 'source', 'amount', 'date', 'income_source']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Filter subcategories (you can also exclude hidden subcategories here if needed)
            hidden_income_ids = list(
                UserHiddenIncomeSubCategory.objects.filter(user=user, hidden=True)
                .values_list('subcategory_id', flat=True)
            )
            self.fields['subcategory'].queryset = IncomeSubCategory.objects.filter(
                models.Q(user=user) | models.Q(user__isnull=True)
            ).exclude(id__in=hidden_income_ids)

            # Filter wallets (exclude system + hidden)
            hidden_wallet_ids = list(
                UserHiddenWallet.objects.filter(user=user, hidden=True)
                .values_list('wallet_id', flat=True)
            )
            self.fields['income_source'].queryset = ExpenseSource.objects.filter(
                models.Q(user=user) | models.Q(user__isnull=True)
            ).exclude(id__in=hidden_wallet_ids)



# forms.py
from django import forms
from .models import ExpenseSource, Income
from django.db import models

class StartingBalanceForm(forms.Form):
    wallet = forms.ModelChoiceField(
        queryset=None,  # we’ll set this in __init__
        label="Wallet",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Amount (KES)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5000'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
        if user:
            # Get IDs of hidden wallets
            hidden_wallet_ids = UserHiddenWallet.objects.filter(user=user, hidden=True).values_list('wallet_id', flat=True)
    
            # Filter wallets: user/global, exclude system wallets and hidden wallets
            self.fields['wallet'].queryset = ExpenseSource.objects.filter(
                models.Q(user=user) | models.Q(user__isnull=True)
            ).exclude(
                models.Q(id__in=hidden_wallet_ids)
            ).order_by('name')

from .utils import get_user_subcategories

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['subcategory', 'description', 'amount', 'date', 'source']  # category removed

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['subcategory'].queryset = get_user_subcategories(user)


            # --- Wallets (exclude hidden) ---
            hidden_wallet_ids = UserHiddenWallet.objects.filter(user=user, hidden=True).values_list('wallet_id', flat=True)
            self.fields['source'].queryset = ExpenseSource.objects.filter(
                Q(user__isnull=True) | Q(user=user) | Q(user__is_superuser=True)
            ).exclude(id__in=hidden_wallet_ids)


class SavingsGoalForm(forms.ModelForm):
    source = forms.ModelChoiceField(
        queryset=ExpenseSource.objects.none(),
        required=True,
        label="Wallet",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_source_id'  # ðŸ‘ˆ this is key for JS to find the dropdown
        })
    )

    class Meta:
        model = SavingsGoal
        fields = ['subcategory', 'target_amount', 'saved_so_far', 'deadline', 'source']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # --- Filter subcategories under 'Savings' only ---
            savings_category = ExpenseCategory.objects.filter(name="Savings", user=user).first()
            if savings_category:
                self.fields['subcategory'].queryset = ExpenseSubCategory.objects.filter(
                    category=savings_category,
                    user=user
                )
            else:
                self.fields['subcategory'].queryset = ExpenseSubCategory.objects.none()

            # --- Filter wallets (exclude system + hidden) ---
            hidden_wallet_ids = UserHiddenWallet.objects.filter(user=user, hidden=True).values_list('wallet_id', flat=True)

            self.fields['source'].queryset = ExpenseSource.objects.filter(
                (models.Q(user=user) | models.Q(user__is_superuser=True) | models.Q(user__isnull=True))
            ).exclude(id__in=hidden_wallet_ids)


class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = ['month', 'category', 'subcategory', 'forecasted_amount']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # ✅ MAIN CATEGORY DROPDOWN
            self.fields['category'].queryset = ExpenseCategory.objects.filter(
                    Q(user__isnull=True) | Q(user=user) | Q(user__is_superuser=True)
            ).order_by('name')

            # ✅ SUBCATEGORY DROPDOWN
            self.fields['subcategory'].queryset = get_user_subcategories(user).filter(
                Q(category__user=user) | Q(category__user__isnull=True)
            ).order_by('category__name', 'name')




class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            })
        }



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


from django import forms
from .models import LoanAccount, LoanPayment

class LoanAccountForm(forms.ModelForm):
    class Meta:
        model = LoanAccount
        fields = ['name', 'principal', 'annual_interest_rate', 'term_periods', 'payment_frequency', 'start_date']


class LoanPaymentForm(forms.ModelForm):
    class Meta:
        model = LoanPayment
        fields = ['amount', 'date', 'is_extra_payment']

# forms.py
from .models import InvestmentAccount
import yfinance as yf
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import InvestmentTransaction



ASSET_CHOICES = [
    ('sacco', 'Sacco / Chama'),
    ("mmf", "Money Market Fund"),
    ("stock", "Stock / ETF"),
    ("crypto", "Cryptocurrency"),
    ("bond", "Bond"),
    ("real_estate", "Real Estate"),
    ("other", "Other"),
]

FREQUENCY_CHOICES = [
    ("annual", "Annual"),
    ("semi_annual", "Semi-Annual"),
    ("quarterly", "Quarterly"),
    ("monthly", "Monthly"),
]


class InvestmentAccountForm(forms.ModelForm):
    asset_type = forms.ChoiceField(choices=ASSET_CHOICES, required=True)

    # Stock / Crypto
    symbol = forms.CharField(required=False, max_length=10)

    # Manual / Non-feed Assets
    manual_price = forms.DecimalField(required=False, max_digits=20, decimal_places=2)
    manual_currency = forms.CharField(required=False, max_length=5)

    units_held = forms.DecimalField(required=False, max_digits=12, decimal_places=4)  # For stocks/MMFs 

    # Bond fields
    face_value = forms.DecimalField(required=False, max_digits=20, decimal_places=2)
    coupon_rate = forms.DecimalField(required=False, max_digits=5, decimal_places=2)
    issue_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    interest_frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES, required=False)
    maturity_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    is_callable = forms.BooleanField(required=False, label="Callable before maturity")

    # MMF / Real Estate fields
    yield_rate = forms.DecimalField(required=False, max_digits=5, decimal_places=2)
    rental_income = forms.DecimalField(required=False, max_digits=20, decimal_places=2)
    expenses = forms.DecimalField(required=False, max_digits=20, decimal_places=2)

    income_so_far = forms.DecimalField(required=False, max_digits=20, decimal_places=2)
    expenses_so_far = forms.DecimalField(required=False, max_digits=20, decimal_places=2)


    # SACCO-specific fields
    sacco_capital_share = forms.DecimalField(required=False, max_digits=12, decimal_places=2)
    sacco_minimum_contribution = forms.DecimalField(required=False, max_digits=12, decimal_places=2)
    sacco_total_contributions = forms.DecimalField(required=False, max_digits=12, decimal_places=2)
    sacco_dividends_earned = forms.DecimalField(required=False, max_digits=12, decimal_places=2)
    sacco_contribution_frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES, required=False)
    sacco_dividend_frequency = forms.ChoiceField(choices=FREQUENCY_CHOICES, required=False)

    class Meta:
        model = InvestmentAccount
        fields = [
            "name", "asset_type", "symbol", "units_held",
            "manual_price", "manual_currency",
            "face_value", "coupon_rate", "issue_date", "interest_frequency", "maturity_date", "is_callable",
            "yield_rate", "rental_income", "expenses", "base_date", "income_so_far", "expenses_so_far",
            "sacco_capital_share", "sacco_minimum_contribution", "sacco_total_contributions", "sacco_dividends_earned",
            "sacco_contribution_frequency", "sacco_dividend_frequency",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make all fields not required by default
        for field in self.fields.values():
            field.required = False

        data = self.data or self.initial
        asset_type = data.get('asset_type')

        # Conditionally require fields
        if asset_type in ['stock', 'crypto']:
            self.fields['symbol'].required = True

        elif asset_type == 'bond':
            for f in ['units_held', 'face_value', 'coupon_rate', 'issue_date', 'maturity_date']:
                self.fields[f].required = True

        elif asset_type == 'mmf':
            self.fields['manual_price'].required = True
            self.fields['yield_rate'].required = True
            self.fields['base_date'].required = True


        elif asset_type in ['real_estate', 'other']:
            self.fields['manual_price'].required = True
            self.fields['income_so_far'].required = True
            self.fields['expenses_so_far'].required = True

        elif asset_type == 'sacco':
            for f in ['sacco_capital_share', 'sacco_minimum_contribution', 'sacco_total_contributions', 'sacco_dividends_earned',
                      'sacco_contribution_frequency', 'sacco_dividend_frequency']:
                self.fields[f].required = True


    def clean(self):
        cleaned_data = super().clean()
        asset_type = cleaned_data.get('asset_type')

        # Server-side validation
        if asset_type in ['stock', 'crypto']:
            if not cleaned_data.get('symbol'):
                self.add_error('symbol', 'Ticker / Symbol is required.')

            # Convert units_held to Decimal, default to 0 if empty
            units = cleaned_data.get('units_held')
            if units in [None, '']:
                cleaned_data['units_held'] = Decimal('0')
            else:
                try:
                    cleaned_data['units_held'] = Decimal(units)
                except InvalidOperation:
                    self.add_error('units_held', 'Enter a valid number.')


        if asset_type == 'bond':
            for field in ['units_held', 'face_value', 'coupon_rate', 'issue_date', 'maturity_date']:
                value = cleaned_data.get(field)
                if value in [None, '']:  # allows 0 but not empty
                    self.add_error(field, f'Please provide a value for {self.fields[field].label}.')

        if asset_type == 'mmf' and not cleaned_data.get('yield_rate'):
            self.add_error('yield_rate', 'Yield rate is required.')

        if asset_type in ['real_estate', 'other'] and not cleaned_data.get('manual_price'):
            self.add_error('manual_price', 'Please provide a value for Price.')

        if asset_type == 'sacco':
            numeric_fields = ['sacco_capital_share', 'sacco_minimum_contribution', 'sacco_dividends_earned', 'sacco_total_contributions']
            choice_fields = ['sacco_contribution_frequency', 'sacco_dividend_frequency']

            for f in numeric_fields:
                if cleaned_data.get(f) is None:  # only None means missing
                    self.add_error(f, f"Please provide a value for {self.fields[f].label}.")


            for f in choice_fields:
                if not cleaned_data.get(f):  # empty choice is invalid
                    self.add_error(f, f"Please provide a value for {self.fields[f].label}.")

        return cleaned_data


class InvestmentTransactionForm(forms.ModelForm):
    action = forms.ChoiceField(choices=[], widget=forms.Select(attrs={"class": "form-select"}))

    class Meta:
        model = InvestmentTransaction
        fields = ["date", "action", "units", "price_per_unit", "amount", "wallet"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "units": forms.NumberInput(attrs={"class": "form-control"}),
            "price_per_unit": forms.NumberInput(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "wallet": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # 👈 pass in request.user
        account = kwargs.pop("account", None)
        super().__init__(*args, **kwargs)

        if user:
            hidden_wallet_ids = UserHiddenWallet.objects.filter(
                user=user, hidden=True
            ).values_list('wallet_id', flat=True)
        
            self.fields["wallet"].queryset = ExpenseSource.objects.filter(
                Q(user=user) | Q(user__isnull=True)
            ).exclude(
                Q(user__is_superuser=True)
                | Q(id__in=hidden_wallet_ids)
            ).distinct().order_by("name")

        if account:
            # Stocks
            if account.asset_type == "stock":
                self.fields["action"].choices = [
                    ("BUY", "Buy Shares"),
                    ("SELL", "Sell Shares"),
                    ("DIVIDEND", "Dividend Payment"),
                ]
                self.fields["units"].label = "Number of Shares"
                self.fields["price_per_unit"].label = "Price per Share"
                self.fields["amount"].label = "Total Transaction Value"

            # Bonds
            elif account.asset_type == "bond":
                self.fields["action"].choices = [
                    ("BUY", "Buy Bond"),
                    ("SELL", "Sell Bond"),
                    ("INTEREST", "Interest Payment"),
                ]
                self.fields["units"].label = "Number of Bonds"
                self.fields["price_per_unit"].label = "Price per Bond"
                self.fields["amount"].label = "Total Transaction Value"

            # Real Estate
            elif account.asset_type == "real_estate":
                self.fields["action"].choices = [
                    ("DEPOSIT", "Add to Property Investment"),
                    ("WITHDRAW", "Withdraw from Property Investment"),
                    ("RENTAL", "Rental Income"),
                    ("EXPENSE", "Property Expense"),
                ]
                self.fields["amount"].label = "Amount (KES)"
                self.fields["units"].widget = forms.HiddenInput()
                self.fields["price_per_unit"].widget = forms.HiddenInput()

            # Money Market Fund
            elif account.asset_type == "mmf":
                self.fields["action"].choices = [
                    ("DEPOSIT", "Deposit Funds"),
                    ("WITHDRAW", "Withdraw Funds"),
                    ("INTEREST", "Interest Earned"),
                ]
                self.fields["amount"].label = "Transaction Amount"
                self.fields["units"].widget = forms.HiddenInput()
                self.fields["price_per_unit"].widget = forms.HiddenInput()

            # Crypto
            elif account.asset_type == "crypto":
                self.fields["action"].choices = [
                    ("BUY", "Buy Crypto"),
                    ("SELL", "Sell Crypto"),
                ]
                self.fields["units"].label = "Units (Coins/Tokens)"
                self.fields["price_per_unit"].label = "Price per Coin/Token"
                self.fields["amount"].label = "Total Transaction Value"

            # Other Investments
            elif account.asset_type == "other":
                self.fields["action"].choices = [
                    ("DEPOSIT", "Add Funds"),
                    ("WITHDRAW", "Withdraw Funds"),
                    ("INTEREST", "Income Received"),
                    ("EXPENSE", "Expense"),
                ]
                self.fields["amount"].label = "Transaction Amount"
                self.fields["units"].widget = forms.HiddenInput()
                self.fields["price_per_unit"].widget = forms.HiddenInput()

            # SACCO
            elif account.asset_type == "sacco":
                self.fields["action"].choices = [
                    ("CONTRIBUTION", "Contribution"),
                    ("DIVIDEND", "Dividend Received"),
                    ("CAPITAL_SHARE", "Add to Capital Shares"),
                ]
                self.fields["amount"].label = "Transaction Amount"
                self.fields["units"].widget = forms.HiddenInput()
                self.fields["price_per_unit"].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get("action")
        units = cleaned_data.get("units")
        price_per_unit = cleaned_data.get("price_per_unit")

        # For BUY/SELL, enforce units and price
        if action in ["BUY", "SELL"]:
            if units is None or units <= 0:
                self.add_error("units", "Units must be greater than zero.")
            if price_per_unit is None or price_per_unit <= 0:
                self.add_error("price_per_unit", "Price per unit must be greater than zero.")

        return cleaned_data



class UpdateInvestmentForm(forms.ModelForm):
    # Only fields relevant for manual updates
    current_price = forms.DecimalField(
        max_digits=20, decimal_places=2, required=True, label="Current Price / NAV"
    )
    face_value = forms.DecimalField(
        max_digits=20, decimal_places=2, required=False, label="Face Value / Nominal Value"
    )
    coupon_rate = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False, label="Coupon Rate (%)"
    )
    interest_frequency = forms.ChoiceField(
        choices=[("annual", "Annual"), ("semi", "Semi-Annual"), ("quarterly", "Quarterly")],
        required=False,
        label="Interest Payment Frequency"
    )
    maturity_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    yield_rate = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False, label="Yield / Interest Rate (%)"
    )
    rental_income = forms.DecimalField(max_digits=20, decimal_places=2, required=False)
    expenses = forms.DecimalField(max_digits=20, decimal_places=2, required=False)

    class Meta:
        model = InvestmentAccount
        fields = [
            "current_price", "face_value", "coupon_rate", "issue_date", "interest_frequency", "maturity_date", "is_callable",
            "yield_rate", "rental_income", "expenses"
        ]

from django import forms
from .models import WalletTransfer, ExpenseSource

from django.db.models import Q
from .models import ExpenseSource, UserHiddenWallet

class WalletTransferForm(forms.ModelForm):
    class Meta:
        model = WalletTransfer
        fields = ["from_wallet", "to_wallet", "amount", "date", "note"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            hidden_wallet_ids = UserHiddenWallet.objects.filter(user=user, hidden=True).values_list('wallet_id', flat=True)
            qs = ExpenseSource.objects.filter(
                Q(user=user) | Q(user__isnull=True)
            ).exclude(
                Q(id__in=hidden_wallet_ids)
            ).order_by("name")

            self.fields["from_wallet"].queryset = qs
            self.fields["to_wallet"].queryset = qs

        # Optional: add Bootstrap classes
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-control"})
