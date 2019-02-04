
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import POS

from ..import_randomization_list import import_randomization_list
from ..models import RandomizationList
from ..randomization import Randomization
from .create_test_list import create_test_list
from .models import RegisteredSubject, MaternalConsent, Appointment, MaternalVisit, MaternalEligibility, AntenatalEnrollment
from .models import MaternalRando


class TestRandomization(TestCase):

    import_randomization_list = False

    def setUp(self):
        super(TestRandomization, self).setUp()
        subject_identifier = '085-0000000'
        self.maternal_eligibility = MaternalEligibility.objects.create(
            report_datetime=get_utcnow(),
            age_in_years=25
        )
        self.maternal_consent = MaternalConsent.objects.create(
            subject_identifier=subject_identifier,
            consent_datetime=get_utcnow() - relativedelta(days=10),
            dob=(get_utcnow() - relativedelta(years=23)).date())
        maternal_consent_model = 'td_rando.maternalconsent'
        Randomization.maternal_consent_model = maternal_consent_model
 
        self.registered_subject = RegisteredSubject.objects.create(
            subject_identifier=subject_identifier)
        registered_subject_model = 'td_rando.registeredsubject'
        Randomization.registered_subject_model = registered_subject_model
 
        self.antenatal_enrollment = AntenatalEnrollment.objects.create(
            report_datetime=get_utcnow(),
            subject_identifier=subject_identifier,
            enrollment_hiv_status=POS
        )
 
        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000')
 
        self.maternal_visit = MaternalVisit.objects.create(
            subject_identifier=appointment.subject_identifier,
            appointment=appointment)
 
    def populate_list(self):
        path = create_test_list()
        import_randomization_list(path=path, overwrite=True)
 
    @tag('r')
    def test_randomization_return(self):
        self.populate_list()
        rando_list = RandomizationList.objects.all()
        self.assertEqual(rando_list.count(), 10)
        options = {'maternal_visit': self.maternal_visit}
        maternal_rando = MaternalRando.objects.create(**options)
        print(maternal_rando.site, maternal_rando.sid, maternal_rando.rx, maternal_rando.subject_identifier,
             maternal_rando.randomization_datetime, maternal_rando.initials)
