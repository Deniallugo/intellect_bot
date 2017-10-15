from django.db import models, transaction
from django.utils.text import slugify
from unidecode import unidecode

from .bot_message import BotMessage


class Question(BotMessage):
    # main = models.BooleanField(default=False)
    # main_type = models.ForeignKey('self')
    name = models.CharField(max_length=255)
    translate = models.SlugField('Транслитерация', max_length=100, blank=True,
                                 unique=True, db_index=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        while not self.translate:
            self.translate = slugify(unidecode(self.name))
            try:
                with transaction.atomic():
                    super(Question, self).save()
                    break
            except:
                result = Question.objects.filter(
                    translate__contains=self.translate).order_by(
                    'translate')[:1].values_list('translate', flat=True)[0]
                try:
                    self.translate = result + '-1'
                except IndexError:
                    pass
        super(Question, self).save()
