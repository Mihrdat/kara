from django.db import models
from django.utils.translation import gettext as _


class OrderStatus(models.IntegerChoices):
    PENDING = 1, _('Pending'),
    PROCESSING = 2, _('Processing')
    AWAITING_FULFILLMENT = 3, _('Awaiting Fulfillment')
    PARTIALLY_FULFILLED = 4, _('Partially Fulfilled')
    FULFILLED = 5, _('Fulfilled')
    SHIPPED = 6, _('Shipped')
    OUT_FOR_DELIVERY = 7, _('Out For Delivery')
    DELIVERED = 8, _('Delivered')
    CANCELLED = 9, _('Cancelled')
    REFUNDED = 10, _('Refunded')
    ON_HOLD = 11, _('On Hold')
    RETURNED = 12, _('Returned')
    EXCHANGE_REQUESTED = 13, _('Exchange Requested')
    COMPLETED = 14, _('Completed')
    DISPUTE = 15, _('Dispute')
