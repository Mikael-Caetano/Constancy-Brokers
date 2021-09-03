# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from palladris_brokers.apps.user.models import User


class Provider(models.Model):
    name = models.CharField(max_length=200, unique=True)
    acronym = models.CharField(max_length=4, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"

    def __str__(self):
        return f"{self.name} - {self.acronym}"


class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    acronym = models.CharField(max_length=3, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.name} - {self.acronym}"


class Pair(models.Model):
    from_currency = models.OneToOneField(Currency, on_delete=models.CASCADE, related_name="pair_from_currency")
    to_currency = models.OneToOneField(Currency, on_delete=models.CASCADE, related_name="pair_to_currency")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pair"
        verbose_name_plural = "Pairs"
        unique_together = ("from_currency", "to_currency")

    def __str__(self):
        return f"{self.from_currency.acronym}/{self.to_currency.acronym}"

    @property
    def get_joined_acronyms(self):
        """Returns the union from the currencies iniciales."""
        return f"{self.from_currency.acronym}/{self.to_currency.acronym}"


class Trade(models.Model):
    trader = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = "Trade"
        verbose_name_plural = "Trades"
        ordering = ["-date"]

    def __str__(self):
        return f""
