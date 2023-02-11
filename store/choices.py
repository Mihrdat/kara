from django.db import models
from django.utils.translation import gettext as _


class OrderStatus(models.IntegerChoices):
    PENDING = 1, _('Pending')
    PROCESSING = 2, _('Processing')
    AWAITING_FULFILLMENT = 3, _('Awaiting Fulfillment')
    FULFILLED = 4, _('Fulfilled')
    SHIPPED = 5, _('Shipped')
    DELIVERED = 6, _('Delivered')
    CANCELLED = 7, _('Cancelled')
    REFUNDED = 8, _('Refunded')
    ON_HOLD = 9, _('On Hold')
    RETURNED = 10, _('Returned')
    EXCHANGE_REQUESTED = 11, _('Exchange Requested')
    COMPLETED = 12, _('Completed')


STATUS_TRANSITION_DIAGRAM = {
    OrderStatus.PENDING: [
        OrderStatus.CANCELLED,
        OrderStatus.REFUNDED,
        OrderStatus.ON_HOLD,
        OrderStatus.PROCESSING,
    ],
    OrderStatus.PROCESSING: [
        OrderStatus.CANCELLED,
        OrderStatus.REFUNDED,
        OrderStatus.ON_HOLD,
        OrderStatus.AWAITING_FULFILLMENT,
        OrderStatus.FULFILLED,
    ],
    OrderStatus.AWAITING_FULFILLMENT: [
        OrderStatus.CANCELLED,
        OrderStatus.REFUNDED,
        OrderStatus.FULFILLED,
    ],
    OrderStatus.FULFILLED: [
        OrderStatus.CANCELLED,
        OrderStatus.REFUNDED,
        OrderStatus.SHIPPED,
    ],
    OrderStatus.SHIPPED: [
        OrderStatus.CANCELLED,
        OrderStatus.REFUNDED,
        OrderStatus.DELIVERED,
    ],
    OrderStatus.DELIVERED: [
        OrderStatus.RETURNED,
        OrderStatus.EXCHANGE_REQUESTED,
        OrderStatus.COMPLETED,
    ],
    OrderStatus.CANCELLED: [],
    OrderStatus.REFUNDED: [],
    OrderStatus.ON_HOLD: [
        OrderStatus.CANCELLED,
        OrderStatus.PROCESSING,
    ],
    OrderStatus.RETURNED: [
        OrderStatus.CANCELLED,
        OrderStatus.REFUNDED,
        OrderStatus.PROCESSING,
    ],
    OrderStatus.EXCHANGE_REQUESTED: [
        OrderStatus.CANCELLED,
        OrderStatus.REFUNDED,
        OrderStatus.PROCESSING,
    ],
    OrderStatus.COMPLETED: []
}


def is_valid_status_transition(current_status, new_status):
    return new_status in STATUS_TRANSITION_DIAGRAM[current_status]
