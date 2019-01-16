
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.utils import get_utcnow
from edc_constants.constants import FAILED_ELIGIBILITY, OFF_STUDY, SCHEDULED, POS, YES, NO, NEG, NOT_APPLICABLE
from edc_constants.constants import SCREENED, UNKNOWN
from edc_registration.models import RegisteredSubject

from edc_meta_data.models import RequisitionMetaData

from ..import_randomization_list import import_randomization_list
from ..models import RandomizationList
from ..randomization import Randomization
from .models import MaternalRando
from .models import RegisteredSubject, MaternalConsent, Appointment, MaternalVisit


class TestRandomization(TestCase):

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

    def hiv_pos_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': POS,
                   'evidence_hiv_status': YES,
                   'will_get_arvs': YES,
                   'is_diabetic': NO,
                   'will_remain_onstudy': YES,
                   'rapid_test_done': NOT_APPLICABLE,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=25)).date()}
        return options

    def hiv_neg_mother_options(self, registered_subject):
        options = {'registered_subject': registered_subject,
                   'current_hiv_status': UNKNOWN,
                   'evidence_hiv_status': None,
                   'week32_test': YES,
                   'week32_test_date': (get_utcnow() - relativedelta(weeks=4)).date(),
                   'week32_result': NEG,
                   'evidence_32wk_hiv_status': YES,
                   'will_get_arvs': NOT_APPLICABLE,
                   'rapid_test_done': YES,
                   'rapid_test_result': NEG,
                   'last_period_date': (get_utcnow() - relativedelta(weeks=34)).date()}
        return options
