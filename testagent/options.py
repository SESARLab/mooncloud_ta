from __future__ import absolute_import

__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'
'''
Project: testagent
Author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
Date: 20/04/15
'''
from tornado.options import define
from tornado.options import options
DEFAULT_CONFIG_FILE = '/etc/testagent/testagent.conf'
DEFAULT_SELFASSESSMENT_DIR = '/etc/testagent/selfassessment'
DEFAULT_EVIDENCES_DIR = '/var/log/testagent/evidences'
DEFAULT_MAIN_LOGFILE = '/var/log/testagent/testagent.log'
CELERY_LOGFILE = '/var/log/testagent/celery.log'

'''
configuration args
'''
define("conf", default=DEFAULT_CONFIG_FILE, help="Configuration file", group="main")


'''
subscription service settings
'''

define("subscription_port", default=8081,
       help="Subscription service listening port", type=int, group="subscription service")
define("subscription_address", default='',
       help="Subscription service listening address", type=str, group="subscription service")
define("subscription_server_cert", type=str, default=None,
       help="SSL certificate file for the subscription service", group="subscription service")
define("subscription_server_key", type=str, default=None,
       help="SSL key file for the subscription service", group="subscription service")
define("subscription_client_ca", type=str, default=None,
       help="SSL Certification Authority for TLS client authentication", group="subscription service")



'''
apis service settings
'''
define("apis_port", default=8080,
       help="APIs listening port", type=int, group="apis service")
define("apis_address", default='0.0.0.0',
       help="APIs listening address", type=str, group="apis service")
define("apis_server_cert", type=str, default=None,
       help="SSL certificate file", group="apis service")
define("apis_server_key", type=str, default=None,
       help="SSL key file", group="apis service")
define("apis_client_ca", type=str, default=None,
       help="SSL Certification Authority for TLS client authentication", group="apis service")

'''
self assessment
'''
define("selfassessment_dir", default=DEFAULT_SELFASSESSMENT_DIR, help="Directory where to grab configurations from", group="self assessment")


'''
events management
'''
define("enable_events", type=bool, default=True,
       help="Periodically enable Celery events" , group="main")
define("persistent", type=bool, default=True,
       help="Enable persistent mode", group="events")
define("inspect_timeout", default=1000, type=float,
       help="Inspect timeout (in milliseconds)", group="events")
define("max_tasks", type=int, default=10000,
       help="Maximum number of tasks to keep in memory", group="main")
define("db", type=str, default='/etc/testagent/testagent.db',
       help="Database file", group="events")

'''
configuration for celery
'''
define("timezone", default="Europe/Rome", help="Timezone (default: Europe/Rome)", type=str, group="main")


define("debug", default=False,
       help="Run in debug mode", type=bool, group="main")
define("evidences_directory", default=DEFAULT_EVIDENCES_DIR,
       help="Log directory for evidences", type=str, group="main")
define("evidences_syslog_server",
       help="Syslog server address", type=str, group="main")
define("evidences_syslog_port", default=514,
       help="Syslog server address", type=int, group="main")
define("evidences_log_level", default="info",
       help="Evidences log level", type=str, group="main")


default_options = options