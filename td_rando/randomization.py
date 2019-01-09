from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from edc_constants.constants import POS
from .constants import RANDOMIZED
from .models import RandomizationItem


class Randomization(object):

    def __init__(self, td_rando, exception_cls=None):
        self.td_rando = td_rando
        self.exception_cls = exception_cls
        self.site = None
        self.sid = None
        self.rx = None
        self.subject_identifier = None
        self.randomization_datetime = None
        self.initials = None

    @property
    def registered_subject_model_cls(self):
        return django_apps.get_model('edc_registration.registeredsubject')

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model('td_maternal.subjectconsent')

    def randomize(self):
        """Selects the next available record from the Pre-Populated Randomization list.
        Update the record with subject_identifier, initials and other maternal specific data."""

        self.verify_hiv_status()
        if self.td_rando.__class__.objects.all().count() == 0:
            next_to_pick = 1
        else:
            next_to_pick = self.td_rando.__class__.objects.all(
            ).order_by('-sid').first().sid + 1
        next_randomization_item = RandomizationItem.objects.get(
            name=str(next_to_pick))
        subject_identifier = self.td_rando.maternal_visit.subject_identifier
        try:
            consent = self.subject_consent_model_cls.objects.filter(
                subject_identifier=subject_identifier).first()
        except ObjectDoesNotExist:
            raise Exception(
                'Object Not Found')
        self.site = consent.study_site
        self.sid = int(next_randomization_item.name)
        self.rx = next_randomization_item.field_name
        self.subject_identifier = subject_identifier
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
        return (self.site, self.sid, self.rx, self.subject_identifier, self.randomization_datetime, self.initials)

    def verify_hiv_status(self):
        if self.td_rando.antenatal_enrollment.enrollment_hiv_status != POS:
            raise self.exception_cls("Cannot Randomize mothers that are not HIV POS. Got {}. See Antenatal Enrollment."
                                     .format(self.td_rando.antenatal_enrollment.enrollment_hiv_status))
