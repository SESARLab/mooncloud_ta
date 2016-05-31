from __future__ import absolute_import

__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'
'''
Project: testagent
Author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
Date: 13/05/15
'''
from tornado.options import define
DEFAULT_SUBSCRIPTION_FILE = '/etc/testagent/subscription.conf'

define("subscription_conf", default=DEFAULT_SUBSCRIPTION_FILE, help="Subscription settings", group="subscription")

define("broker_url",
       help="Broker URL", type=str, group="communication")
define("broker_ssl_enable", type=bool, default=False, help="Enables SSL", group="communication")
define("broker_ssl_ca", type=str, help="Certification authority for SSL",  group="communication")
define("broker_ssl_verifycert", type=str,
       help="Enables SSL Certificate verification",  group="communication")
define("broker_ssl_keyfile",
       help="SSL Key Path",
       type=str, group="communication")
define("broker_ssl_certfile",
       help="SSL Certificate Path",
       type=str, group="communication")

define("backend_broker_url", default="", help="Backend broker URL", type=str, group="communication")

define("tasks_exchange_name", default="celery", help="Exchange name for sending tasks (default: celery)", type=str, group="communication")
define("tasks_exchange_type", default="direct", help="Exchange type for sending tasks (default: direct)", type=str, group="communication")
define("tasks_queue_name", default="celery", help="Queue name for sending tasks (default: celery)", type=str, group="communication")
define("tasks_routing_key", default="celery", help="Routing key for sending tasks", type=str, group="communication")


define("results_exchange_name", default="collector_agents",
       help="Exchange name for reporting results (default: collector_agents)", type=str, group="communication")
define("results_exchange_type", default="direct",
       help="Exchange type for reporting results (default: direct)",type=str, group="communication")
define("results_queue_name", default="celery", group="communication")
define("results_routing_key", default="key-test",
       help="Routing key for reporting results (default: key-test)", type=str, group="communication")