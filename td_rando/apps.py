#import os

from django.apps import AppConfig as DjangoAppConfig
#from django.conf import settings
#from django.core.checks.registry import register


class AppConfig(DjangoAppConfig):
    name = 'td_rando'
    include_in_administration = False
