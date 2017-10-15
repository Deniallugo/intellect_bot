from django.db import models

from .message_button import MessageButton
from .telegram_file import TelegramFile


class BotMessage(models.Model):
    text = models.TextField(null=True)
    type = models.CharField(max_length=255, default='')
    file = models.ForeignKey(TelegramFile,
                             related_name='message_file',
                             null=True, blank=True)
    disable_notification = models.BooleanField(default=True)
    buttons = models.ManyToManyField(MessageButton, blank=True)

    class Meta:
        verbose_name = "Сообщение бота"
        verbose_name_plural = "Сообщения бота"

    def __str__(self):
        return self.type

    def check_response(self, text_response):
        find_response = [item for item in self.buttons.all()
                         if item.text == text_response]

        return find_response if find_response else None
