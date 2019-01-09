from django.db import import models
from edc_base.model_mixins import BaseUuidModel


class MaternalRando (BaseUuidModel):
    
    subject_identifier = models.CharField(max_length=25)
    
    report_datetime = models.DateTimeField()
    
    site = models.CharField(max_length=25)
    
    sid = models.DecimalField(
        max_digits=5,
        decimal_places=2)
    
    rx=models.Charfield(max_length=25)
    
    randomization_datetime=models.DateTimeField()
    
    initials=models.Charfield(max_length=25)
    