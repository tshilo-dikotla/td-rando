
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import POS

from ..import_randomization_list import import_randomization_list
from ..models import RandomizationList
from ..randomization import Randomization
from .create_test_list import create_test_list
from .models import MaternalRando
from .models import RegisteredSubject, MaternalConsent, Appointment, MaternalVisit, MaternalEligibility, AntenatalEnrollment


class TestRandomization(TestCase):

    import_randomization_list = False

    def populate_list(self):
        path = create_test_list(first_sid=1)
        import_randomization_list(path=path, overwrite=True)

    def create_participant(self, subject_identifier=None):
        MaternalEligibility.objects.create(
            report_datetime=get_utcnow(),
            age_in_years=25
        )
        MaternalConsent.objects.create(
            subject_identifier=subject_identifier,
            consent_datetime=get_utcnow() - relativedelta(days=10),
            dob=(get_utcnow() - relativedelta(years=23)).date(),
            initials='LL')
        subject_consent_model = 'td_rando.maternalconsent'
        Randomization.subject_consent_model = subject_consent_model

        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier)
        registered_subject_model = 'td_rando.registeredsubject'
        Randomization.registered_subject_model = registered_subject_model

        AntenatalEnrollment.objects.create(
            report_datetime=get_utcnow(),
            subject_identifier=subject_identifier,
            enrollment_hiv_status=POS
        )

        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000')

        maternal_visit = MaternalVisit.objects.create(
            subject_identifier=appointment.subject_identifier,
            appointment=appointment)

        return maternal_visit

    @tag('r')
    def test_randomization_return(self):
        self.populate_list()

        rando_list = RandomizationList.objects.all().order_by('sid')
        self.assertEqual(rando_list.count(), 10)

        count = 1
        for x in rando_list:
            options = {'maternal_visit': self.create_participant(
                subject_identifier='085-0000000-' + str(count))}
            maternal_rando = MaternalRando.objects.create(**options)
            self.assertEqual(maternal_rando.sid, count)
            count += 1
