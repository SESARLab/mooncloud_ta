from __future__ import absolute_import
from __future__ import print_function

__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'
'''
Project: testagent
Author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
Date: 20/04/15
'''

import sys
import signal
import tornado.log

from tornado.options import options
from tornado.options import parse_command_line, parse_config_file
from tornado.log import enable_pretty_logging
from tornado import ioloop
from celery.bin.base import Command
from testagent import __version__
from testagent.options import DEFAULT_CONFIG_FILE
from testagent.subscription_options import DEFAULT_SUBSCRIPTION_FILE
from testagent.services.SubscriptionService import TestAgentSubscription
from testagent.services.ApiService import TestAgentAPI
from testagent.services.WorkerService import WorkerService, WorkerServiceException
from testagent.services.LoggingService import LoggingService
from testagent.selfassessment import SelfAssessment
import daemon, daemon.pidfile

def sigterm_handler(signum, frame):
    LoggingService().get_generic_logger().warning('SIGTERM detected, shutting down')
    sys.exit(0)

class TestAgentCommand(Command):

    def run_from_argv(self, prog_name, argv=None, command=None):

        argv = list(filter(self.testagent_option, argv))

        try:
            parse_config_file(options.conf, final=False)
        except IOError:
            if options.conf != DEFAULT_CONFIG_FILE:
                raise
        try:
            parse_config_file(options.subscription_conf, final=False)
        except IOError:
            if options.subscription_conf != DEFAULT_SUBSCRIPTION_FILE:
                raise

        parse_command_line([prog_name] + argv)

        #
        # DEBUG MODE LOGGING
        #
        if options.debug and options.logging == 'info':
            options.logging = "debug"
            enable_pretty_logging()

        LoggingService().setup_logger()
        pidfile = daemon.pidfile.PIDLockFile("/var/run/testagent.pid")
        context = daemon.DaemonContext(pidfile=pidfile, files_preserve=[LoggingService().get_file_handler().stream])
        context.signal_map = {
            signal.SIGTERM: sigterm_handler
        }
        with context:
            try:
                LoggingService().configure(options)
                logger = LoggingService().get_generic_logger()
                SelfAssessment().configure(options.selfassessment_dir)
                TestAgentSubscription().configure(options, logger)
                TestAgentAPI().configure(options, self.app, logger)
                TestAgentSubscription().start()
                TestAgentAPI().start()
                WorkerService().configure(self.app, options)
                try:
                    WorkerService().start_worker()
                except WorkerServiceException:
                    logger.warning("Worker not configured. Use Subscription APIs to configure it.")

                io_loop = ioloop.IOLoop.instance()
                io_loop.start()
            except (KeyboardInterrupt, SystemExit):
                sys.exit(0)

    def handle_argv(self, prog_name, argv, command=None):
        return self.run_from_argv(prog_name, argv)

    def early_version(self, argv):
        if '--version' in argv:
            print(__version__, file=self.stdout)
            super(TestAgentCommand, self).early_version(argv)

    @staticmethod
    def testagent_option(arg):
        name, _, value = arg.lstrip('-').partition("=")
        name = name.replace('-', '_')
        return hasattr(options, name)