from .common import *

SECRET_KEY = 'django-insecure-v*!upq!^puv^gzfj6&lnssm5q7iu2jgl$vue=iqwe!x*@z#3^$'

DEBUG = True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
}
