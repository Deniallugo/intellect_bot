from django.contrib.postgres.fields import JSONField
from django.db import models

from .question import Question
from .user import TelegramUser


class OrderType(models.Model):
    name = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question)


class Order(models.Model):
    type = models.ForeignKey(OrderType)
    user = models.ForeignKey(TelegramUser)
    sent = models.BooleanField(default=False)
    property_json = JSONField(null=True, default={})

    def check_order_status(self) -> Question:

        all_fields = list(
            self.type.questions.all().values_list(
                'translate', flat=True))
        try:
            question_key = set(all_fields).difference(set(list(
                self.property_json.keys()
            ) or [])).pop()
            print(question_key)
            question = Question.objects.get(translate=question_key)
            return question
        except:
            return None

    def set_property(self, field, value):
        self.property_json[field.translate] = value
        self.save()
