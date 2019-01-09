from django.db import import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


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

class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appt_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25)

    visit_instance = models.CharField(max_length=25)
    
class MaternalVisit(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)
    
class RegisteredSubject(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50,
        unique=True)

    relative_identifier = models.CharField(
        max_length=36,
        null=True,
        blank=True)

class MaternalConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    consent_datetime = models.DateTimeField()

    dob = models.DateField()            
    