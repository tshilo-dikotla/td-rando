from django.conf import settings

if settings.APP_NAME == 'td_rando':
    from .tests import models
