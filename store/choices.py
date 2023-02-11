from django.db import models
from django.utils.translation import gettext as _

"""
1.  Pending: The order has been placed, but payment has not been confirmed.
2.  Processing: Payment has been confirmed and the order is being prepared for shipment.
3.  Awaiting fulfillment: The order is waiting to be fulfilled, either because the required items are out of stock or because additional information is needed.
4.  Fulfilled: All items in the order have been fulfilled and are ready to be shipped.
5.  Shipped: The order has been shipped and is on its way to the customer.
6.  Delivered: The order has been delivered to the customer.
7.  Cancelled: The order has been cancelled either by the customer or by the retailer.
8.  Refunded: The customer has requested a refund and it has been processed.
9.  On hold: The order has been put on hold for further review or due to a problem with payment.
10. Returned: The customer has returned the order and it is waiting to be processed by the retailer.
11. Exchange requested: The customer has requested to exchange the order for a different item.
12. Completed: The order has been successfully completed, and the customer is satisfied with their purchase.
"""


class OrderStatus(models.IntegerChoices):
    PENDING = 0, _('Pending')
    PROCESSING = 1, _('Processing')
    AWAITING_FULFILLMENT = 2, _('Awaiting Fulfillment')
    FULFILLED = 3, _('Fulfilled')
    SHIPPED = 4, _('Shipped')
    DELIVERED = 5, _('Delivered')
    CANCELLED = 6, _('Cancelled')
    REFUNDED = 7, _('Refunded')
    ON_HOLD = 8, _('On Hold')
    RETURNED = 9, _('Returned')
    EXCHANGE_REQUESTED = 10, _('Exchange Requested')
    COMPLETED = 11, _('Completed')


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


def map_status(status):
    if status in [
        OrderStatus.PENDING,
        OrderStatus.PROCESSING,
        OrderStatus.AWAITING_FULFILLMENT,
        OrderStatus.FULFILLED,
    ]:
        return OrderStatus.labels[OrderStatus.PENDING]

    return OrderStatus.labels[status]
