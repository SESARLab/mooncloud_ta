from __future__ import absolute_import

__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'
'''
Project: testagent
Author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
Date: 20/05/15
'''

import logging
import atexit
import tornado.web

from functools import partial
from concurrent.futures import ThreadPoolExecutor
from tornado.httpserver import HTTPServer
from ssl import CERT_REQUIRED

from testagent.utils.Singleton import Singleton
from testagent.services.handlers.ApiServiceHandlers import handlers
from testagent.options import default_options
from testagent.utils import abs_path
from testagent.events import Events

from testagent.exceptions.ApiServiceException import ApiServiceException

class TestAgentAPI(tornado.web.Application, Singleton):
    pool_executor_cls = ThreadPoolExecutor
    max_workers = 4
    started = False

    def __init__(self, **kwargs):
        Singleton.__init__(self)

    def configure(self, options, capp, logger, **kwargs):
        Singleton.configure(self)
        self.logger = logger
        self.options = options if options else default_options
        self.ssl = None
        if options.apis_server_cert and options.apis_server_key:
            self.ssl = dict(
                certfile=abs_path(options.apis_server_cert),
                keyfile=abs_path(options.apis_server_key)
            )
            if options.apis_client_ca:
                self.ssl["ca_certs"] = abs_path(options.apis_client_ca)
                self.ssl["cert_reqs"] = CERT_REQUIRED

        tornado.web.Application.__init__(self, debug=options.debug, handlers=handlers)
        self.capp = capp
        self.events = Events(self.capp,
                                        db=self.options.db,
                                        persistent=self.options.persistent,
                                        enable_events=self.options.enable_events,
                                        max_tasks_in_memory=self.options.max_tasks,
                                        logger=self.logger)
        self.started = False
        atexit.register(self.stop)
        self.http_server = HTTPServer(self, ssl_options=self.ssl)

    @Singleton._if_configured(ApiServiceException)
    def start(self):
        self.pool = self.pool_executor_cls(max_workers=self.max_workers)
        self.events.start()
        self.logger.info("APIs available at http%s://%s:%s" % ('s' if self.ssl else '', self.options.apis_address, self.options.apis_port))
        self.listen(self.options.apis_port,
                    address=self.options.apis_address,
                    ssl_options=self.ssl,
                    xheaders=True
                    )

        self.started = True

    @Singleton._if_configured(ApiServiceException)
    def stop(self):
        if self.started:
            self.events.stop()
            self.pool.shutdown(wait=False)
            self.started = False

    @Singleton._if_configured(ApiServiceException)
    def delay(self, method, *args, **kwargs):
        return self.pool.submit(partial(method, *args, **kwargs))

    @property
    @Singleton._if_configured(ApiServiceException)
    def transport(self):
        return getattr(self.capp.connection().transport,
                       driver_type=None)
