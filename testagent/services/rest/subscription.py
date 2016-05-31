from __future__ import absolute_import

__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'
'''
Project: testagent
Author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
Date: 11/05/15
'''
from testagent.api.ViewBaseHandler import BaseHandler
from tornado.web import HTTPError
from tornado.escape import json_decode
from testagent.services.WorkerService import WorkerService, WorkerServiceException
import logging
import json

logger = logging.getLogger("SubscriptionAPIs")

class BaseTaskHandler(BaseHandler):
    def get_task_args(self):
        try:
            body = self.request.body
            options = json_decode(body) if body else {}
        except ValueError as e:
            raise HTTPError(400, str(e))
        args = options.pop('args', [])
        kwargs = options.pop('kwargs', {})

        if not isinstance(args, (list, tuple)):
            raise HTTPError(400, 'args must be an array')

        return args, kwargs, options

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)

    def safe_result(self, result):
        "returns json encodable result"
        try:
            json.dumps(result)
        except TypeError:
            return repr(result)
        else:
            return result

class SubscriptionService2(BaseTaskHandler):
    def get(self, ciao=None, **kwargs):
        print ciao
        print "kwargs"
        print kwargs
        self.write({"status":"ok"})

class SubscriptionService(BaseTaskHandler):
    def post(self):
        result = dict()
        options = WorkerService().get_options()
        default_opts = options.group_dict("communication")
        for item in default_opts:
            result[item] = self.get_body_argument(item, default=default_opts[item])

            if result[item] is None:
                result[item] = ""
            else:
                result[item] = str(result[item])

        output_file = options.subscription_conf
        out = open(output_file, "w")
        for item in result:
            if result[item].isdigit() or result[item] == "True" or result[item] == "False":
                out.write(item + " = " + result[item] + "\n")
            elif result[item] and result[item].replace(" ", "") != "":
                out.write(item + " = \"" + result[item] + "\"\n")
        out.close()

        '''
        cp = SafeConfigParser(allow_no_value=True)

        try:
            cp.read(output_file + "3")
        except:
            pass

        try:
            cp.add_section('subscription')
        except DuplicateSectionError:
            pass

        for item in result:
            cp.set('subscription', item, unicode(result[item]))
        try:
            with open(output_file + "3", "w") as output_file_opened:
                cp.write(output_file_opened)
        except IOError:
            raise Exception("Can't open configuration file for writing")
        '''
        app = WorkerService().get_app()
        try:
            WorkerService().stop_worker()
        except:
            pass
        try:
            WorkerService().deconfigure()
        except:
            pass
        from tornado.options import parse_config_file
        # parse_config_file("testagent/utils/subscription_config.py")
        parse_config_file(output_file)
        WorkerService().configure(app, options)
        try:
            WorkerService().start_worker()
        except WorkerServiceException:
            logger.warning("Worker not configured. Use Subscription APIs again to configure it.")

        self.write(options.group_dict("communication"))

