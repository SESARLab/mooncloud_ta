from __future__ import absolute_import

__author__ = 'patrizio'

from testagent.services.rest import subscription

handlers = [
    (r"/", subscription.SubscriptionService),
    (r"/test", subscription.SubscriptionService2)
]