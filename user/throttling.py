from rest_framework.throttling import AnonRateThrottle


class SendOTPAnonRateThrottle(AnonRateThrottle):
    rate = "2/minute"
