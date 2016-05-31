from __future__ import absolute_import

__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'
'''
Project: testagent
Author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
Date: 20/04/15
'''
from oslo.config import cfg

CONF = cfg.CONF
DEFAULT_CONFIG_FILE = 'testagent.conf'
DEFAULT_SUBSCRIPTION_FILE = 'subscription4.conf'
DEFAULT_SELFASSESSMENT_DIR = '/etc/testagent/selfassessment'
DEFAULT_EVIDENCES_DIR = 'var/log/testagent/evidences'
DEFAULT_MAIN_LOGFILE = 'var/log/testagent/testagent.log'


main = [
    cfg.StrOpt('log-level', default='info', help="Log level")
]

CONF.register_opts(main)

subscription_service = cfg.OptGroup(name='subscription', title='Subscription service options')
subscription_service_opts = [
    cfg.IntOpt('port', default=8080, help="Listening port"),
    cfg.IPOpt("address", default='0.0.0.0', help="Listening address"),
    cfg.StrOpt("server_cert",  default=None, help="SSL certificate file"),
    cfg.StrOpt("server_key",  default=None, help="SSL key file"),
    cfg.StrOpt("client_ca",  default=None, help="SSL Certification Authority for TLS client authentication"),
]

CONF.register_group(subscription_service)
CONF.register_opts(subscription_service_opts, subscription_service)

apis_service = cfg.OptGroup(name='apis_service', title='APIs service options')
apis_service_opts = [
    cfg.IntOpt('port', default=8081, help="Listening port"),
    cfg.IPOpt("address", default='0.0.0.0', help="Listening address"),
    cfg.StrOpt("server_cert",  default=None, help="SSL certificate file"),
    cfg.StrOpt("server_key",  default=None, help="SSL key file"),
    cfg.StrOpt("client_ca",  default=None, help="SSL Certification Authority for TLS client authentication"),
]

CONF.register_group(apis_service)
CONF.register_opts(apis_service_opts, apis_service)

self_assessment = cfg.OptGroup(name='selfassessment', title='Self-assessment')
self_assessment_opts = [
    cfg.StrOpt("directory", default=DEFAULT_SELFASSESSMENT_DIR, help="Directory where to grab configurations from")
]

CONF.register_group(self_assessment)
CONF.register_opts(self_assessment_opts, self_assessment)

events = cfg.OptGroup(name='worker', title="Worker options")
events_opts = [
    cfg.BoolOpt("enable-events", default=True, help="Periodically enable Celery events"),
    cfg.BoolOpt("persistent", default=True, help="Enable persistent mode"),
    cfg.FloatOpt("inspect-timeout", default=1000, help="Inspect timeout (in milliseconds)"),
    cfg.IntOpt("max-tasks", default=10000, help="Maximum number of tasks to keep in memory"),
    cfg.StrOpt("db", default="testagent.db", help="Database file"),
    cfg.StrOpt("timezone", default="Europe/Rome", help="Timezone (default: Europe/Rome)")
]

CONF.register_group(events)
CONF.register_opts(events_opts, events)

evidences = cfg.OptGroup(name='evidences', title="Evidences")
evidences_opts = [
    cfg.StrOpt("directory", default=DEFAULT_EVIDENCES_DIR,
           help="Directory for evidences"),
    cfg.StrOpt("syslog_server",
           help="Syslog server address"),
    cfg.IntOpt("syslog_port", default=514,
           help="Syslog server port"),
    cfg.StrOpt("log_level", default="info",
           help="Evidences log level")
]

CONF.register_group(evidences)
CONF.register_opts(evidences_opts, evidences)

broker = cfg.OptGroup(name='broker', title="Broker settings")
broker_opts = [
    cfg.StrOpt("url", help="Broker URL"),
    cfg.BoolOpt("ssl_enable",  default=False, help="Enables SSL"),
    cfg.StrOpt("ssl_ca",  help="Certification authority for SSL"),
    cfg.StrOpt("ssl_verifycert",  help="Enables SSL Certificate verification"),
    cfg.StrOpt("ssl_keyfile", help="SSL Key Path"),
    cfg.StrOpt("ssl_certfile", help="SSL Certificate Path"),
    cfg.StrOpt("backend_url", default="", help="Backend broker URL")
]

CONF.register_group(broker)
CONF.register_opts(broker_opts, broker)


tasks = cfg.OptGroup(name='tasks', title="Task RabbitMQ settings")
tasks_opts = [
    cfg.StrOpt("exchange_name", default="celery", help="Exchange name for sending tasks (default: celery)"),
    cfg.StrOpt("exchange_type", default="direct", help="Exchange type for sending tasks (default: direct)"),
    cfg.StrOpt("queue_name", default="celery", help="Queue name for sending tasks (default: celery)"),
    cfg.StrOpt("routing_key", default="celery", help="Routing key for sending tasks"),
]

CONF.register_group(tasks)
CONF.register_opts(tasks_opts, tasks)


results = cfg.OptGroup(name='results', title="Results RabbitMQ settings")
results_opts = [
    cfg.StrOpt("exchange_name", default="collector_agents", help="Exchange name for sending tasks (default: celery)"),
    cfg.StrOpt("exchange_type", default="direct", help="Exchange type for sending tasks (default: direct)"),
    cfg.StrOpt("queue_name", default="celery", help="Queue name for sending tasks (default: celery)"),
    cfg.StrOpt("routing_key", default="key-test", help="Routing key for sending tasks")
]

CONF.register_group(results)
CONF.register_opts(results_opts, results)