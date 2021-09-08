import random
import decimal
from django.conf import settings
from celery import task

from .models import Provider, Pair, Trade
from constancy_brokers.apps.user.models import User


@task()
def generate_trades():
    """Generate random trades for the sake of testing."""

    traders = User.objects.all()
    providers = Provider.objects.all()
    pairs = Pair.objects.all()

    trades = []

    random_traders = random.choices(traders, k=settings.TRADES_CREATED_PER_MINUTE)
    random_providers = random.choices(providers, k=settings.TRADES_CREATED_PER_MINUTE)
    random_pairs = random.choices(pairs, k=settings.TRADES_CREATED_PER_MINUTE)

    for user, provider, pair in zip(random_traders, random_providers, random_pairs):
        quantity = random.randint(1, 1000)

        last_trade = (
            Trade.objects.filter(trader=user, provider=provider, pair=pair)
            .order_by("-date")
            .first()
        )

        if last_trade:
            random_price_change = decimal.Decimal(random.uniform(-10, +10))
            price = max(last_trade.price + random_price_change, 0)
        else:
            price = random.uniform(0.1, 1000)

        trades.append(
            Trade(
                trader=user,
                provider=provider,
                pair=pair,
                quantity=quantity,
                price=price,
            )
        )

    Trade.objects.bulk_create(trades)

    print(f"Trades created sucessfully.")
    return
