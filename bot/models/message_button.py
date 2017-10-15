from django.db import models


class MessageButton(models.Model):
    text = models.CharField(max_length=255)
    inline = models.BooleanField(default=False)
    data = models.CharField(max_length=65, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    next_state = models.CharField(max_length=255, null=True,
                                  blank=True)  # предназначен для таблицы переходов

    class Meta:
        verbose_name = "Кнопка Сообщений"
        verbose_name_plural = "Кнопки Сообщений"
