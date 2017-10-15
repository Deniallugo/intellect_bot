from django.db import models


class TelegramFile(models.Model):
    telegram_id = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(null=True, upload_to='uploads/%Y/%m/%d/')
    file_type = models.CharField(max_length=255, null=True, default='photo')

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def save(self, *args, **kwargs):
        if not self.telegram_id:
            self.telegram_id = None
        super(TelegramFile, self).save(*args, **kwargs)

    def __str__(self):
        return u'%s' % (self.file.url)
