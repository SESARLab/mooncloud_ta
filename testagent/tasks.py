# -*- coding: utf-8 -*-

from __future__ import absolute_import

from testagent.parser import CollectorParser
from celery import Task
from testagent.structure import Collector
from testagent.exceptions.ParserException import ParserException
from testagent.exceptions.ProbeExecutionError import ProbeExecutionError
from testagent.services.WorkerService import WorkerService
from testagent.services.LoggingService import LoggingService
from celery.utils.log import get_task_logger

import logging, logging.handlers
import importlib
import sys

app = WorkerService()


class StreamToLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())


@app.app.task
class start_certification(Task):
    @property
    def log(self):
        return self.logger

    def run(self, xml):
        ls = LoggingService()
        self.logger = get_task_logger('%s.%s#%s' % (__name__, self.__class__.__name__, str(self.request.id)))

        str_log_level = ls.get_parameter("evidences_log_level")

        loglevels = {
            "info": logging.INFO,
            "debug": logging.DEBUG,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }

        self.logger.setLevel(loglevels[str_log_level])
        evidences_dir = ls.get_parameter('evidences_directory')
        evidences_dir = evidences_dir if evidences_dir[-1] == "/" else evidences_dir + "/"
        evidences_file = str(self.request.id) + ".log"

        file = logging.FileHandler(evidences_dir + evidences_file)
        file.setLevel(loglevels[str_log_level])
        file.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file)
        if ls.get_parameter("evidences_use_syslog"):
            syslog = logging.handlers.SysLogHandler(address=(ls.get_parameter("evidences_syslog_server"), ls.get_parameter("evidences_syslog_port")))
            syslog.setLevel(loglevels[str_log_level])
            syslog.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(syslog)

        oldstdout = sys.stdout
        oldstderr = sys.stderr
        sys.stdout = StreamToLogger(self.logger, logging.INFO)
        sys.stderr = StreamToLogger(self.logger, logging.ERROR)

        results = []
        current_testcase = 0

        try:
            cp = CollectorParser()
            cp.set_input(xml)
            my_collector = cp.parse()
        except:
            self.log.warning("Unable to parse XML - abort")
            raise

        if not my_collector or not isinstance(my_collector, Collector):
            raise ParserException("This should never happen")

        try:
            probe = importlib.import_module("testagent.probes." + my_collector.getTot())
        except IOError:
            raise ProbeExecutionError(my_collector.getTot() + " No such file or directory")
        except:
            raise

        all_testcases = len(my_collector.getTestcases())
        for testcase in my_collector.getTestcases():
            this_probe = probe.probe()
            this_probe.appendAtomics()
            this_probe.setLogger(self.log)

            testcase_result = this_probe.run(self, current_testcase + 1, all_testcases, testcase)
            results.append(testcase_result)
            current_testcase += 1
        sys.stdout = oldstdout
        sys.stderr = oldstderr
        return results
