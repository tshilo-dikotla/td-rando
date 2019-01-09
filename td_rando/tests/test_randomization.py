

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.utils import get_utcnow
from td_maternal.tests.base_test_case import BaseTestCase

from ..import_randomization_list import import_randomization_list
from ..models import RandomizationList
from ..randomization import Randomization
from .models import MaternalRando
from .models import RegisteredSubject, MaternalConsent, Appointment, MaternalVisit


class TestRandomization(BaseTestCase):

    def setUP(self):
        subject_identifier = '085-0000000'
        relative_identifier = '085-0000000-10'
        appointment = Appointment.objects.create(
            subject_identifier=subject_identifier,
            appt_datetime=get_utcnow(),
            visit_code='2000')
        self.maternal_visit = MaternalVisit.objects.create(
            subject_identifier=appointment.subject_identifier,
            appointment=appointment)
        RegisteredSubject.objects.create(
            subject_identifier=subject_identifier,
            relative_identifier=relative_identifier)
        registered_subject_model = 'td_rando.registeredsubject'
        Randomization.registered_subject_model =\
            registered_subject_model
        self.maternal_consent = MaternalConsent.objects.create(
            subject_identifier=relative_identifier,
            consent_datetime=get_utcnow() - relativedelta(days=10),
            dob=(get_utcnow() - relativedelta(years=23)).date())
        maternal_consent_model = 'td_rando.maternalconsent'
        Randomization.maternal_consent_model =\
            maternal_consent_model
