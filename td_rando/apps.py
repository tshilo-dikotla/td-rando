from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'td_rando'
    include_in_administration = False
    antenatal_enrollement_model = 'td_rando.antenatalenrollment'
