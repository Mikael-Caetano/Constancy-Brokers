# *-* coding: utf-8 *-*
from django.core.management.base import BaseCommand
from django.conf import settings

import names
import random
import string

from palladris_brokers.apps.trade.models import (
    Provider,
    Currency,
    Pair,
)
from palladris_brokers.apps.user.models import User


class Command(BaseCommand):
    help = "Creates base providers, currencies and set the created currencies pairs."

    def handle(self, *args, **options):
        try:
            random_traders_first_names = [
                names.get_first_name() for i in range(settings.BASE_TRADERS)
            ]
            random_traders_last_names = [
                names.get_last_name() for i in range(settings.BASE_TRADERS)
            ]

            random_providers_names = [
                names.get_full_name() for i in range(settings.BASE_PROVIDERS)
            ]

            random_currencies_names = [
                names.get_full_name() for i in range(settings.BASE_CURRENCIES)
            ]

            traders = []
            for first_name, last_name in zip(
                random_traders_first_names, random_traders_last_names
            ):
                username = self.get_random_username(first_name, last_name)
                email = self.get_random_email(first_name, last_name)
                password = self.get_random_password(8)
                traders.append(
                    User(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=password,
                    )
                )

            # The user password is not being hashed for the sake of testing, thus you can check the password on django admin.
            User.objects.bulk_create(traders)

            providers = []
            for name in random_providers_names:
                acronym = self.get_name_acronym(name)
                providers.append(Provider(name=name, acronym=acronym))

            Provider.objects.bulk_create(providers)

            currencies = []
            for name in random_currencies_names:
                acronym = self.get_name_acronym(name)
                currencies.append(Currency(name=name, acronym=acronym))

            Currency.objects.bulk_create(currencies)

            created_currencies = Currency.objects.all()
            pairs = []
            for from_currency in created_currencies:
                for to_currency in created_currencies.exclude(id=from_currency.id):
                    if not Pair.objects.filter(
                        from_currency=from_currency, to_currency=to_currency
                    ).exists():
                        pairs.append(
                            Pair(from_currency=from_currency, to_currency=to_currency)
                        )

            Pair.objects.bulk_create(pairs)

            print(f"Base instances created sucessfully!")

        except Exception as e:
            print(f"Error while creating base instances -> {e}")

    def get_name_acronym(self, name):
        name_letters = name.replace(" ", "")
        letter_quantity = len(name_letters)
        middle_name_letter = name_letters[int((letter_quantity / 2))]
        acronym = name_letters[0] + middle_name_letter + name_letters[-1]
        return acronym.upper()

    def get_random_username(self, first_name, last_name):
        return (first_name + "_" + last_name).lower()

    def get_random_email(self, first_name, last_name):
        return (first_name + last_name).lower() + "@genericmail.com"

    def get_random_password(self, length):
        lower_letters = string.ascii_lowercase
        password = "".join(random.choice(lower_letters) for i in range(length))
        return password