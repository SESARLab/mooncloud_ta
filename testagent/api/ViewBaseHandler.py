from __future__ import absolute_import

__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'
'''
Project: testagent
Author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
Date: 20/04/15
'''

import tornado
import inspect
import traceback

from distutils.util import strtobool
from testagent.utils import template

class BaseHandler(tornado.web.RequestHandler):
    def render(self, *args, **kwargs):
        functions = self._get_template_functions()
        assert not set(map(lambda x: x[0], functions)) & set(kwargs.keys())
        kwargs.update(functions)
        super(BaseHandler, self).render(*args, **kwargs)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            message = None
            if 'exc_info' in kwargs and\
                    kwargs['exc_info'][0] == tornado.web.HTTPError:
                    message = kwargs['exc_info'][1].log_message
            self.render('404.html', message=message)
        elif status_code == 500:
            error_trace = ""
            for line in traceback.format_exception(*kwargs['exc_info']):
                error_trace += line

            self.finish('Error 500')
        elif status_code == 401:
            self.set_status(status_code)
            self.set_header('WWW-Authenticate', 'Basic realm="flower"')
            self.finish('Access denied')
        else:
            message = None
            if 'exc_info' in kwargs and\
                    kwargs['exc_info'][0] == tornado.web.HTTPError:
                    message = kwargs['exc_info'][1].log_message
                    self.set_header('Content-Type', 'text/plain')
                    self.write(message)
            self.set_status(status_code)

    def get_argument(self, name, default=[], strip=True, type=None):
        arg = super(BaseHandler, self).get_argument(name, default, strip)
        if type is not None:
            try:
                if type is bool:
                    arg = strtobool(str(arg))
                else:
                    arg = type(arg)
            except (ValueError, TypeError):
                if arg is None and default is None:
                    return arg
                raise tornado.web.HTTPError(
                    400,
                    "Invalid argument '%s' of type '%s'" % (
                        arg, type.__name__))
        return arg

    @property
    def capp(self):
        "return Celery application object"
        return self.application.capp

    @staticmethod
    def _get_template_functions():
        return inspect.getmembers(template, inspect.isfunction)