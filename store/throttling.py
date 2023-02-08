from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class CartAnonRateThrottle(AnonRateThrottle):
    rate = '10/minute'


class CartUserRateThrottle(UserRateThrottle):
    rate = '1000/hour'
