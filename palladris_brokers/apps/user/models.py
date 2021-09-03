from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser): 
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"