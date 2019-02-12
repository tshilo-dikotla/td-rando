from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from edc_constants.constants import POS

from .constants import RANDOMIZED
from .models import RandomizationList


class Randomization(object):

    subject_consent_model = 'td_maternal.subjectconsent'
    registered_subject_model = 'edc_registration.registeredsubject'
    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def registered_subject_model_cls(self):
        return django_apps.get_model(self.registered_subject_model)

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model(self.subject_consent_model)

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def __init__(self, td_rando=None, exception_cls=None):
        self.td_rando = td_rando
        self.exception_cls = exception_cls
        self.subject_identifier = td_rando.maternal_visit.appointment.subject_identifier
        self.site = None
        self.sid = None
        self.rx = None
        self.randomization_datetime = None
        self.initials = None

    def randomize(self):
        """Selects the next available record from the Pre-Populated Randomization list.
        Update the record with subject_identifier, initials and other maternal specific data."""

        self.verify_hiv_status()
        if self.td_rando.__class__.objects.all().count() == 0:
            next_to_pick = 1
        else:
            next_to_pick = self.td_rando.__class__.objects.all(
            ).order_by('-sid').first().sid + 1
        next_randomization_item = RandomizationList.objects.get(
            sid=str(next_to_pick))
        subject_identifier = self.td_rando.maternal_visit.subject_identifier
        try:
            consent = self.subject_consent_model_cls.objects.filter(
                subject_identifier=subject_identifier).first()
        except ObjectDoesNotExist:
            raise Exception(
                'Object Not Found')
        self.site = settings.DEFAULT_STUDY_SITE
        self.sid = int(next_randomization_item.sid)
        self.rx = next_randomization_item.drug_assignment
        self.randomization_datetime = timezone.datetime.now()
        self.initials = consent.initials

        dte = timezone.datetime.today()
        try:
            registered_subject = self.registered_subject_model_cls.objects.get(
                subject_identifier=self.td_rando.maternal_visit.subject_identifier)
        except ObjectDoesNotExist:
            raise Exception(
                'Object Not Found')
        registered_subject.sid = self.sid
        registered_subject.randomization_datetime = self.randomization_datetime
        registered_subject.modified = dte
        registered_subject.registration_status = RANDOMIZED
        registered_subject.save()
        return (self.site, self.sid,
                self.rx, self.subject_identifier,
                self.randomization_datetime, self.initials)

    @property
    def antenatal_enrollment(self):
        """Return antenatal enrollment.
        """
        try:
            antenatal_enrollment = self.antenatal_enrollment_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            raise ValidationError(
                f'Antenatal Enrollment for subject {self.subject_identifier} must exist')
        return antenatal_enrollment

    def verify_hiv_status(self):
        if self.antenatal_enrollment.enrollment_hiv_status != POS:
            raise self.exception_cls(
                'Cannot Randomize mothers that are not HIV POS. '
                f'Got {self.antenatal_enrollment.enrollment_hiv_status}. See Antenatal Enrollment.')
