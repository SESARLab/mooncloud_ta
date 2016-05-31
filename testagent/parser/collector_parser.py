#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of cumulus-testagent.
# https://github.com/patriziotufarolo/cumulus-testagent

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>

from lxml import etree

from testagent.parser import Parser
from testagent.parser.testcase_parser import TestCaseParser

from testagent.parser.exceptions import CollectorParsingException
from testagent.structure import Collector


class CollectorParser(Parser):
    def parse(self):
        try:
            root = etree.fromstring(self.get_input().encode('utf-8'), parser=etree.XMLParser(encoding='utf-8'))
        except etree.XMLSyntaxError as e:
            raise CollectorParsingException(e)

        if root.tag.lower() == "collector":
            if (not root.get("id")) or root.get("id") == "":
                raise CollectorParsingException("id parameter has not been defined for the collector")
            else:
                collector_id = root.get("id")

            if not root.get("cmid") or root.get("cmid") == "":
                raise CollectorParsingException("cmid parameter has not been defined for the collector")
            else:
                cm_id = root.get("cmid")

            if not root.get("probe_driver") or root.get("probe_driver") == "":
                raise CollectorParsingException("probe_driver parameter has not been defined for the collector")
            else:
                tot = root.get("probe_driver")

            inside = (root.text if root.text is not None else '') + ''.join(
                etree.tostring(child, pretty_print=False, method='c14n') for child in root)
            collector_obj = Collector(collector_id, cm_id, tot)
            tcp = TestCaseParser()
            tcp.set_input(inside)
            tcp.set_probe(tot)
            tcp.set_cm_id(cm_id)
            testcases = tcp.parse()
            for testcase_obj in testcases:
                collector_obj.appendTestCase(testcase_obj)
        else:
            raise CollectorParsingException("Root element is not a Collector tag")
        return collector_obj
