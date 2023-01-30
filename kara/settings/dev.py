from .common import *

SECRET_KEY = 'django-insecure-v*!upq!^puv^gzfj6&lnssm5q7iu2jgl$vue=iqwe!x*@z#3^$'

DEBUG = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'custom.pagination.GlobalLimitOffsetPagination',
}
