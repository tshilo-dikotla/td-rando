from django.utils import timezone
from edc_constants.constants import POS

from td_maternal.models import SubjectConsent

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
        consent = SubjectConsent.objects.filter(
            subject_identifier=subject_identifier).first()
        self.site = consent.study_site
        self.sid = int(next_randomization_item.name)
        self.rx = next_randomization_item.field_name
        self.subject_identifier = subject_identifier
        self.randomization_datetime = timezone.datetime.now()
        self.initials = self.td_rando.maternal_visit.appointment.registered_subject.initials

        dte = timezone.datetime.today()
        registered_subject = self.td_rando.maternal_visit.appointment.registered_subject
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
