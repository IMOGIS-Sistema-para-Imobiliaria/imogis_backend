from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4


class User(AbstractUser):
    class Meta:
        ordering = ["username"]

    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
        editable=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    reset_password = models.BooleanField(default=False)
