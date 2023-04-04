from django.db import models
from django.utils.translation import gettext as _

"""
0. New: The order has been placed, but payment has not been confirmed.
1. Processing: Payment has been confirmed and the order is being prepared for shipment.
2. Fulfilled: All items in the order have been fulfilled and are ready to be shipped.
3. Shipped: The order has been shipped and is on its way to the customer.
4. Delivered: The order has been delivered to the customer.
5. Cancelled: The order has been cancelled either by the customer or by the retailer.
6. Returned: The customer has returned the order and it is waiting to be processed by the retailer.
7. Completed: The order has been successfully completed, and the customer is satisfied with their purchase.
"""


class OrderStatus(models.IntegerChoices):
    NEW = 0, _("New")
    PROCESSING = 1, _("Processing")
    FULFILLED = 2, _("Fulfilled")
    SHIPPED = 3, _("Shipped")
    DELIVERED = 4, _("Delivered")
    CANCELLED = 5, _("Cancelled")
    RETURNED = 6, _("Returned")
    COMPLETED = 7, _("Completed")


STATUS_TRANSITION_DIAGRAM = {
    OrderStatus.NEW: [
        OrderStatus.CANCELLED,
        OrderStatus.PROCESSING,
    ],
    OrderStatus.PROCESSING: [
        OrderStatus.CANCELLED,
        OrderStatus.FULFILLED,
    ],
    OrderStatus.FULFILLED: [
        OrderStatus.CANCELLED,
        OrderStatus.SHIPPED,
    ],
    OrderStatus.SHIPPED: [
        OrderStatus.CANCELLED,
        OrderStatus.DELIVERED,
    ],
    OrderStatus.DELIVERED: [
        OrderStatus.RETURNED,
        OrderStatus.COMPLETED,
    ],
    OrderStatus.CANCELLED: [],
    OrderStatus.RETURNED: [
        OrderStatus.CANCELLED,
        OrderStatus.PROCESSING,
    ],
    OrderStatus.COMPLETED: [],
}


def is_valid_status_transition(current_status, new_status):
    return new_status in STATUS_TRANSITION_DIAGRAM[current_status]


def map_status(status):
    if status in [
        OrderStatus.NEW,
        OrderStatus.PROCESSING,
        OrderStatus.FULFILLED,
    ]:
        return OrderStatus.labels[OrderStatus.NEW]

    return OrderStatus.labels[status]
