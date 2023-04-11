from django.db import models

from helpers import generate_string_uuid_hex


class Wallet(models.Model):
    TYPE = (
        ("Visa", "Visa"),
        ("Mastercard", "Mastercard"),
    )
    CURRENCY = (
        ("USD", "USD"),
        ("RUB", "RUB"),
        ("EUR", "EUR"),
    )

    name = models.CharField(max_length=8, unique=True, default=generate_string_uuid_hex)
    type = models.CharField(max_length=50, choices=TYPE, blank=False)
    currency = models.CharField(max_length=10, choices=CURRENCY, blank=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    owner = models.ForeignKey(
        "auth.User", related_name="wallets", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "wallet"
