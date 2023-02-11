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
