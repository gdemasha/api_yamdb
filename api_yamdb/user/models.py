from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.constants import ROLE_CHOICE


class CustomUser(AbstractUser):
    bio = models.TextField('Био', blank=True)
    role = models.CharField(
        'Выбор пользователя',
        choices=ROLE_CHOICE,
        default='user',
    )
