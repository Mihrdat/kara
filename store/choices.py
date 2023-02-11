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

    @property
    def status_transition_diagram(self):
        return {
            self.PENDING: [
                self.CANCELLED,
                self.REFUNDED,
                self.ON_HOLD,
                self.PROCESSING,
            ],
            self.PROCESSING: [
                self.CANCELLED,
                self.REFUNDED,
                self.ON_HOLD,
                self.AWAITING_FULFILLMENT,
                self.FULFILLED,
            ],
            self.AWAITING_FULFILLMENT: [
                self.CANCELLED,
                self.REFUNDED,
                self.FULFILLED,
            ],
            self.FULFILLED: [
                self.CANCELLED,
                self.REFUNDED,
                self.SHIPPED,
            ],
            self.SHIPPED: [
                self.CANCELLED,
                self.REFUNDED,
                self.DELIVERED,
            ],
            self.DELIVERED: [
                self.RETURNED,
                self.EXCHANGE_REQUESTED,
                self.COMPLETED,
            ],
            self.CANCELLED: [],
            self.REFUNDED: [],
            self.ON_HOLD: [
                self.CANCELLED,
                self.PROCESSING,
            ],
            self.RETURNED: [
                self.CANCELLED,
                self.REFUNDED,
                self.PROCESSING,
            ],
            self.EXCHANGE_REQUESTED: [
                self.CANCELLED,
                self.REFUNDED,
                self.PROCESSING,
            ],
            self.COMPLETED: []
        }


def is_valid_status_transition(current_status, new_status):
    return new_status in OrderStatus.status_transition_diagram[current_status]
