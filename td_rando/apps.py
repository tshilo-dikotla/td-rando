#import os

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
#from django.core.checks.registry import register


class AppConfig(DjangoAppConfig):
    name = 'td_rando'
    include_in_administration = False


if settings.APP_NAME == 'td_rando':
    from edc_visit_tracking.apps import (
        AppConfig as BaseEdcVisitTrackingAppConfig)

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'td_maternal': ('maternal_visit', 'td_maternal.maternalvisit')}
