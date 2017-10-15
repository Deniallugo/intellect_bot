from hashids import Hashids
from django.conf import settings
from django.db import models

from .common import HashableModel
from .telegram_file import TelegramFile


class Company(models.Model):
    hasher = Hashids(
        salt=settings.SALT_COMPANY,
        min_length=8,
        alphabet=settings.ALPHABET_FULL
    )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    category = models.CharField(max_length=255)
    photo = models.ForeignKey(
        TelegramFile,
        related_name='company_photo',
        null=True,
        on_delete=models.SET_NULL
    )

    # users = models.ManyToManyField(
    #     'bot.TelegramUser',
    #     through='bot.UserCompany',
    #     through_fields=('company', 'user')
    # )

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return self.name
