from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from datetime import timedelta
from django.utils import timezone


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
    reset_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code_expires_at = models.DateTimeField(null=True, blank=True)

    def generate_reset_code(self):
        import random
        import string

        code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        self.reset_code = code
        self.reset_code_expires_at = timezone.now() + timedelta(minutes=30)
        self.save()
        return code

    def is_reset_code_valid(self, reset_code):
        if self.reset_code_expires_at is None or self.reset_code is None:
            return False

        if self.reset_code_expires_at < timezone.now():
            return False

        if self.reset_code != reset_code:
            return False

        return True
