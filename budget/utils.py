from decimal import Decimal, getcontext

# Increase precision to avoid rounding issues for long schedules
getcontext().prec = 28

from decimal import Decimal, ROUND_HALF_UP

def loan_amortization_schedule(
    principal, annual_interest_rate, term_periods, payments_per_year,
    extra_payment=Decimal('0'), one_time_extra=Decimal('0'), start_extra_period=0
):
    principal = Decimal(principal)
    annual_interest_rate = Decimal(annual_interest_rate)
    term_periods = int(term_periods)
    payments_per_year = int(payments_per_year)

    # Handle 0% interest case
    if annual_interest_rate == 0:
        payment_per_period = (principal / term_periods).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        rate_per_period = (annual_interest_rate / 100) / payments_per_year
        payment_per_period = (principal * (rate_per_period * (1 + rate_per_period) ** term_periods) /
                              ((1 + rate_per_period) ** term_periods - 1)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    schedule = []
    remaining_balance = principal
    total_interest = Decimal('0')

    for period in range(1, term_periods + 1):
        if annual_interest_rate == 0:
            interest_payment = Decimal('0')
        else:
            interest_payment = (remaining_balance * (annual_interest_rate / 100) / payments_per_year).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        principal_payment = payment_per_period - interest_payment

        # Apply extra payment logic
        if period >= start_extra_period > 0:
            principal_payment += extra_payment
        if period == start_extra_period and one_time_extra > 0:
            principal_payment += one_time_extra

        remaining_balance -= principal_payment
        total_interest += interest_payment

        if remaining_balance < 0:
            principal_payment += remaining_balance
            remaining_balance = Decimal('0')

        schedule.append({
            'period': period,
            'payment': float(payment_per_period),
            'interest': float(interest_payment),
            'principal': float(principal_payment),
            'balance': float(remaining_balance)
        })

        if remaining_balance <= 0:
            break

    payoff_periods = len(schedule)
    return schedule, total_interest, payoff_periods

# utils.py
import yfinance as yf
import requests
from datetime import date
from .models import InvestmentAccount, PriceHistory
from decimal import Decimal

# Mapping from ticker symbols to CoinGecko IDs
COINGECKO_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "DOGE": "dogecoin",
    "ADA": "cardano",
    "SOL": "solana",
    # add more as needed
}

def fetch_stock_price(symbol: str):
    """Fetch stock price and currency from Yahoo Finance."""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        if hist.empty:
            return None, None
        price = hist["Close"].iloc[-1]
        currency = ticker.info.get("currency", "USD")
        return float(price), currency
    except Exception:
        return None, None

def fetch_crypto_price(crypto_id: str, vs: str = "usd"):
    """Fetch latest crypto price in USD from CoinGecko."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={vs}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        price = data.get(crypto_id, {}).get(vs)
        if price is None:
            return None, None
        return float(price), vs.upper()
    except Exception:
        return None, None

def update_prices(user):
    """
    Update today's price for all user accounts.
    Stocks keep their Yahoo currency, cryptos are in USD.
    """
    accounts = InvestmentAccount.objects.filter(
        user=user,
        asset_type__in=["stock", "crypto"]
    )
    updated = []

    for account in accounts:
        price = None
        currency = None

        if account.symbol:
            if account.asset_type == "stock":
                price, currency = fetch_stock_price(account.symbol)
            elif account.asset_type == "crypto":
                crypto_id = COINGECKO_IDS.get(account.symbol.upper())
                if crypto_id:
                    price, currency = fetch_crypto_price(crypto_id)

        if price is not None:
            PriceHistory.objects.update_or_create(
                account=account,
                date=date.today(),
                defaults={
                    "price": Decimal(str(price)),
                    "currency": currency
                }
            )
            updated.append(account.symbol)

    return updated


# utils.py

from django.db.models import Q
from .models import ExpenseSubCategory, UserHiddenSubCategory

def get_user_subcategories(user, category=None):
    # Get IDs of subcategories the user has chosen to hide
    hidden_ids = UserHiddenSubCategory.objects.filter(user=user).values_list('subcategory_id', flat=True)

    # Get global + user-owned subcategories only
    subcategories = ExpenseSubCategory.objects.filter(
        Q(user__isnull=True) | Q(user=user) | Q(user__is_superuser=True)
    ).exclude(id__in=hidden_ids)

    # Optional filter by category (useful for dependent dropdowns)
    if category:
        subcategories = subcategories.filter(category=category)

    return subcategories
