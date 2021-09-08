from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_provider_admin = models.BooleanField(default=False)

    # setting required fields for createsuperuser command.
    REQUIRED_FIELDS = [
        "password",
        "first_name",
        "last_name",
        "email",
        "is_provider_admin",
    ]

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"