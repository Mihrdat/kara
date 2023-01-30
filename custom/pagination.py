from rest_framework.pagination import LimitOffsetPagination


class GlobalLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100
