from __future__ import absolute_import
from functools import wraps
from testagent.exceptions.SingletonException import SingletonException
__author__ = 'patrizio'


class Singleton(object):
    _instances = {}
    _configured = False
    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]

    def configure(self):
        self._configured = True

    def check_configured(self):
        return self._configured

    @staticmethod
    def _if_configured(this_exception):
        if not this_exception or not issubclass(this_exception, SingletonException):
            this_exception = SingletonException

        def _configured_decorator(func):
            @wraps(func)
            def wrapper(inst, *args, **kwargs):
                if not inst.check_configured():
                    raise this_exception("Object not configured properly")
                else:
                    return func(inst, *args, **kwargs)

            return wrapper

        return _configured_decorator
