from django.db import models
from .company import Company


class Address(models.Model):
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return self.name
