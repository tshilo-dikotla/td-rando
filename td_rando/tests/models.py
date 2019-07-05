from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO_UNKNOWN_NA
from td_rando.randomization import Randomization


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


class MaternalConsent(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    consent_datetime = models.DateTimeField()

    dob = models.DateField()

    initials = models.CharField(max_length=4)


class AntenatalVisitMembership(BaseUuidModel):

    report_datetime = models.DateTimeField()

    subject_identifier = models.CharField(max_length=25)

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

    subject_identifier = models.CharField(max_length=25)

    enrollment_hiv_status = models.CharField(max_length=25)


class MaternalRando (BaseUuidModel):

    maternal_visit = models.ForeignKey(MaternalVisit, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    site = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    sid = models.IntegerField(
        null=True,
        blank=True)

    rx = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    randomization_datetime = models.DateTimeField(
        null=True,
        blank=True)

    initials = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    def save(self, *args, **kwargs):
        randomization_helper = Randomization(self)
        (self.site, self.sid, self.rx, self.subject_identifier,
         self.randomization_datetime, self.initials) = randomization_helper.randomize()
        super(MaternalRando, self).save(*args, **kwargs)
