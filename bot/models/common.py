from django.conf import settings
from django.db import models
from hashids import Hashids


class HashableModel(models.Model):
    hash_prefix = ''
    min_length = 4
    alphabet = settings.ALPHABET_SHORT
    hasher = Hashids(
        salt=settings.HASHIDS_SALT,
        alphabet=alphabet,
        min_length=min_length
    )

    @property
    def uid(self):
        return self.hash_prefix + self.hasher.encode(self.pk)

    @classmethod
    def get_from_uid(cls, uid):
        clear_hash = uid[len(cls.hash_prefix):]
        uid = cls.hasher.decode(clear_hash)
        return cls.objects.get(id=cls.hasher.decode(clear_hash)[0])

    class Meta:
        abstract = True
