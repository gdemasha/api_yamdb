from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICE = ('user', 'moderator', 'admin')

    bio = models.CharField('Био', max_length=256, null=True, blank=True,)
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=ROLE_CHOICE,
        default='user',
    )


User = get_user_model()
