from __future__ import absolute_import
from functools import wraps

__author__ = 'patrizio'

import celery.bin.worker

from multiprocessing import Process
from celery import Celery
from celery.signals import task_success, task_failure, task_revoked
from kombu import Queue, Exchange
from ssl import CERT_REQUIRED

from testagent.utils.Singleton import Singleton
from testagent.exceptions.WorkerServiceException import WorkerServiceException
from testagent.options import default_options, CELERY_LOGFILE
import testagent.subscription_options

@task_success.connect
def task_success_handler(sender=None, result=None, args=None, kwargs=None, **kwds):
    ws = WorkerService()
    result_to_send = sender.request.id + "#" + str(result[0])
    print("Sending back: " + result_to_send)
    #queue = Queue('collector_agents',
    #              Exchange("collector_agents", type="direct"),
    #              'key-test')
    exchange = Exchange(ws.CeleryConfiguration.RESULT_EXCHANGE_NAME, type=ws.CeleryConfiguration.RESULT_EXCHANGE_TYPE)
    queue = Queue(ws.CeleryConfiguration.RESULT_QUEUE_NAME,
        exchange=exchange,
        routing_key=ws.CeleryConfiguration.RESULT_ROUTING_KEY
    )

    with ws.app.producer_or_acquire(None) as prod:
        prod.publish(result_to_send, serializer='raw',
                     routing_key=ws.CeleryConfiguration.RESULT_ROUTING_KEY,
                     declare=[queue], exchange=exchange,
                     retry=True)
    print("Sent back: " + result_to_send)


class WorkerService(Singleton):
    status = None
    worker_process = None

    class CeleryConfiguration(object):
        """
            default settings
        """
        CELERY_ACCEPT_CONTENT = ['json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_EVENT_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_IMPORTS = ('testagent.tasks',)
        CELERYD_POOL_RESTARTS = True
        CELERYD_HIJACK_ROOT_LOGGER = False

    def __custom_banner(self):
        RED = "\033[1;49;31m"
        WHITE = "\033[1;49;37m"
        RESET_SEQ = "\033[1;49;37m"
        from celery.apps import worker as celery_worker
        celery_worker.ARTLINES = []

        celery_worker.BANNER = """\n
        \t\t\tCelery Version {version}

        Welcome\t\t\t\t\t""" + RED + """{hostname}"""+RESET_SEQ+"""

        => Test Agent ID:\t\t\t"""+RED+"""{app}"""+RESET_SEQ+"""
        => Broker:\t\t\t\t"""+RED+"""{conninfo}"""+RESET_SEQ+"""
        => Results backend broker:\t\t"""+RED+"""{results}"""+RESET_SEQ+"""
        => Concurrency\t\t\t\t"""+RED+"""{concurrency}"""+RESET_SEQ+"""

        => Active queues
        {queues}
        """

        ARTLINES = [
        RED+'''                                                             .lkKWMWNKx:.                    ''' + RESET_SEQ,
        RED+'''                                                          ;xXMMMMMMMMMMMMKd'                 ''' + RESET_SEQ,
        RED+'''                                                       .dWMMW0          KMMMXl.              ''' + RESET_SEQ,
        RED+'''                                                      xMMM0:              cXMMWl             ''' + RESET_SEQ,
        RED+'''                                         ..,,;,'.   .XMMK,                  ;NMM0.           ''' + RESET_SEQ,
        RED+'''                                     ,o0WMMMMMMMMMXkNMMd                      OMMK           ''' + RESET_SEQ,
        RED+'''                  .;okKXNNX0kl'   .oNMMMXOdc::clx0WMMMk                        0MMd          ''' + RESET_SEQ,
        RED+'''                c0MMMMWXKKXWMMMWkdWMMKc.           ,dK.                       \'MMW          ''' + RESET_SEQ,
        RED+'''              :NMMWx;.      .:OMMMMX;                                           WMMk.        ''' + RESET_SEQ,
        RED+'''             kMMNc             .dWO                                             ;OMMMO.      ''' + RESET_SEQ,
        RED+'''            xMMX.                .                                               .kMMWc      ''' + RESET_SEQ,
        RED+'''           'MMW.                                                                    :WMMl    ''' + RESET_SEQ,
        RED+'''           dMMk                                                                      ;MMM    ''' + RESET_SEQ,
        RED+'''     .cdkOONMMk                                                                       xMMO   ''' + RESET_SEQ,
        RED+'''  .oXMMMMMMMMMN  '''+WHITE+'''                                                               '''+RED+'''      ,MMW   ''' + RESET_SEQ,
        RED+''' ;WMMXl.   .,o0: '''+WHITE+'''                                                               '''+RED+'''      'MMW   ''' + RESET_SEQ,
        RED+''';MMMl            '''+WHITE+'''             TEST BASED CERTIFICATION ENVIRONMENT              '''+RED+'''      lMM0   ''' + RESET_SEQ,
        RED+'''XMMl             '''+WHITE+'''             TEST AGENT  version 1.1 - April 2015              '''+RED+'''     .WMM;   ''' + RESET_SEQ,
        RED+'''WMM'             '''+WHITE+'''    Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>    '''+RED+'''    .XMMx    ''' + RESET_SEQ,
        RED+'''0MMd             '''+WHITE+'''                                                               '''+RED+'''   cWMMd     ''' + RESET_SEQ,
        RED+''''WMMd                                                                           .cXMMK,      ''' + RESET_SEQ,
        RED+''' ;NMMNd;....................................................................,cdKMMM0:        ''' + RESET_SEQ,
        RED+'''  .oNMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWOl.          ''' + RESET_SEQ,
        RED+'''     c0WMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWN0o,              ''' + RESET_SEQ,
        ]

        celery_worker.BANNER = '\n'.join(ARTLINES) + "\n" + celery_worker.BANNER + "\n"

    def configure(self, app=None, options=None):
        options = options if options else default_options
        self.app = app or Celery("testagent")
        if (options
            and options.broker_url
            and options.results_exchange_name
            and options.results_exchange_type
            and options.results_queue_name
            and options.results_routing_key
            and options.tasks_exchange_name
            and options.tasks_exchange_name
            and options.tasks_exchange_type
            and options.tasks_queue_name):

            super(WorkerService, self).configure()

            self.__custom_banner()
            self.status = "stopped"
            self.worker_process = Process()
            print self.CeleryConfiguration
            self.CeleryConfiguration.BROKER_URL = options.broker_url
            self.CeleryConfiguration.CELERY_TIMEZONE = options.timezone
            self.CeleryConfiguration.CELERY_RESULT_BACKEND = options.backend_broker_url
            self.CeleryConfiguration.CELERY_DEFAULT_QUEUE = options.tasks_queue_name
            self.CeleryConfiguration.CELERY_QUEUES = [
                Queue(options.tasks_queue_name,
                      exchange=Exchange(options.tasks_exchange_name, type=options.tasks_exchange_type),
                      routing_key=options.tasks_routing_key
                      )
            ]

            self.CeleryConfiguration.BROKER_USE_SSL = False
            if options.broker_ssl_enable and options.broker_ssl_ca:
                self.CeleryConfiguration.BROKER_USE_SSL = {
                    "ca_certs": options.broker_ssl_cacerts
                }
                if options.broker_ssl_verifycert and options.broker_ssl_keyfile and options.broker_ssl_certfile:
                    self.CeleryConfiguration.BROKER_USE_SSL["keyfile"] = options.broker_ssl_keyfile
                    self.CeleryConfiguration.BROKER_USE_SSL["certfile"] = options.broker_ssl_certfile
                    self.CeleryConfiguration.BROKER_USE_SSL["cert_reqs"] = CERT_REQUIRED

            self.CeleryConfiguration.RESULT_EXCHANGE_NAME = options.results_exchange_name
            self.CeleryConfiguration.RESULT_EXCHANGE_TYPE = options.results_exchange_type
            self.CeleryConfiguration.RESULT_QUEUE_NAME = options.results_queue_name
            self.CeleryConfiguration.RESULT_ROUTING_KEY = options.results_routing_key
            self.app.config_from_object(self.CeleryConfiguration)
            self.app.connection = self.app.broker_connection
            self.app.loader.import_default_modules()
            self.options = options

    @Singleton._if_configured(WorkerServiceException)
    def deconfigure(self):
        self._configured = False

    def get_app(self):
        if self.app:
            return self.app

    @Singleton._if_configured(WorkerServiceException)
    def _worker_thread(self):
        wrk = celery.bin.worker.worker(app=self.app)
        wrk.run(logfile=CELERY_LOGFILE)

    def get_options(self):
        try:
            return self.options if self.options else default_options
        except:
            return default_options

    @Singleton._if_configured(WorkerServiceException)
    def start_worker(self):
        if self.status != "started":
            self.worker_process = Process(target=self._worker_thread)
            self.worker_process.start()
            self.status = "started"

    @Singleton._if_configured(WorkerServiceException)
    def stop_worker(self):
        if self.worker_process.is_alive():
            self.worker_process.terminate()
        if self.status == "started":
            self.status = "stopped"
