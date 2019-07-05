from django.db import models
from django_crypto_fields.fields import EncryptedTextField
from edc_base.model_mixins import BaseUuidModel


class RandomizationList(BaseUuidModel):

    sid = models.IntegerField(
        verbose_name='SID',
        unique=True)

    drug_assignment = EncryptedTextField(
        verbose_name="Treatment Assignment")

    class Meta:
        app_label = 'td_rando'
        verbose_name = 'RandomizationList'
