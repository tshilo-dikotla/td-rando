from asyncio.windows_events import NULL

from django.db import models
from django.db.models.deletion import PROTECT
from django.utils import timezone
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO_UNKNOWN_NA
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


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


class AntenatalVisitMembership(BaseUuidModel):

    report_datetime = models.DateTimeField()

    registered_subject = models.Charfield(
        max_length=50,
        unique=True)
    antenatal_visits = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN_NA
    )


class MaternalUltraSoundIni(BaseUuidModel):

    maternal_visit = models.CharField(
        max_length=15,
        choices=YES_NO_UNKNOWN_NA
    )
    report_datetime = models.DateTimeField()


class MaternalEligibility(BaseUuidModel):

    report_datetime = models.DateTimeField()

    age_in_years = models.DecimalField(
        max_digits=5,
        decimal_places=2)


class AntenatalEnrollment(BaseUuidModel):

    report_datetime = models.DateTimeField()

    registered_subject = models.Charfield(
        max_length=50,
        unique=True)
    current_hiv_status = models.CharField(max_length=25)


class MaternalRando (BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    maternal_visit = models.ForeignKey(MaternalVisit)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    site = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    sid = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True)

    rx = models.Charfield(
        max_length=25,
        null=True,
        blank=True)

    randomization_datetime = models.DateTimeField(
        null=True,
        blank=True)

    initials = models.Charfield(
        max_length=25,
        null=True,
        blank=True)
