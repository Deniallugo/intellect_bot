from django.db import models
from . import TelegramUser
from . import Company


class UserCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    authorized = models.BooleanField(default=False)

    class Meta:
        unique_together = ('company', 'user')
