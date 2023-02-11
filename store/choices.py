from django.db import models
from django.utils.translation import gettext as _


class OrderStatus():
    PENDING = 1
    PROCESSING = 2
    AWAITING_FULFILLMENT = 3
    FULFILLED = 4
    SHIPPED = 5
    DELIVERED = 6
    CANCELLED = 7
    REFUNDED = 8
    ON_HOLD = 9
    RETURNED = 10
    EXCHANGE_REQUESTED = 11
    COMPLETED = 12

    CHOICES = [
        (PENDING, _('Pending')),
        (PROCESSING, _('Processing')),
        (AWAITING_FULFILLMENT, _('Awaiting Fulfillment')),
        (FULFILLED, _('Fulfilled')),
        (SHIPPED, _('Shipped')),
        (DELIVERED, _('Delivered')),
        (CANCELLED, _('Cancelled')),
        (REFUNDED, _('Refunded')),
        (ON_HOLD, _('On Hold')),
        (RETURNED, _('Returned')),
        (EXCHANGE_REQUESTED, _('Exchange Requested')),
        (COMPLETED, _('Completed')),
    ]

    STATUS_TRANSITION_DIAGRAM = {
        PENDING: [
            CANCELLED,
            REFUNDED,
            ON_HOLD,
            PROCESSING,
        ],
        PROCESSING: [
            CANCELLED,
            REFUNDED,
            ON_HOLD,
            AWAITING_FULFILLMENT,
            FULFILLED,
        ],
        AWAITING_FULFILLMENT: [
            CANCELLED,
            REFUNDED,
            FULFILLED,
        ],
        FULFILLED: [
            CANCELLED,
            REFUNDED,
            SHIPPED,
        ],
        SHIPPED: [
            CANCELLED,
            REFUNDED,
            DELIVERED,
        ],
        DELIVERED: [
            RETURNED,
            EXCHANGE_REQUESTED,
            COMPLETED,
        ],
        CANCELLED: [],
        REFUNDED: [],
        ON_HOLD: [
            CANCELLED,
            PROCESSING,
        ],
        RETURNED: [
            CANCELLED,
            REFUNDED,
            PROCESSING,
        ],
        EXCHANGE_REQUESTED: [
            CANCELLED,
            REFUNDED,
            PROCESSING,
        ],
        COMPLETED: []
    }


def is_valid_status_transition(current_status, new_status):
    return new_status in OrderStatus.STATUS_TRANSITION_DIAGRAM[current_status]
