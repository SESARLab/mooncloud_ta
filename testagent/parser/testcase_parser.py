#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of cumulus-testagent.
# https://github.com/patriziotufarolo/cumulus-testagent

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>

from lxml import etree

from testagent.parser import Parser
from testagent.parser.testinstance_parser import TestInstanceParser

from testagent.parser.exceptions import TestCaseParsingException
from testagent.structure import TestCase


class TestCaseParser(Parser):
    def parse(self):
        try:
            root = etree.fromstring(self.get_input())
        except etree.XMLSyntaxError as e:
            raise TestCaseParsingException(e)

        result = []
        if root.tag.lower() == "testcases":
            for element in root:
                testcase_id = ""
                testcase_description = ""
                for subelement in element:
                    if subelement.tag == "ID":
                        testcase_id = subelement.text
                    if subelement.tag == "Description":
                        testcase_description = subelement.text

                if not testcase_id or testcase_id is None or testcase_id == "":
                    raise TestCaseParsingException("ID not found for testcase. Remember: XML is case sensitive.")
                if not testcase_description:
                    testcase_description = ""
                tc = TestCase(testcase_id, testcase_description)
                tip = TestInstanceParser()
                tip.set_probe(self.get_probe())
                tip.set_cm_id(self.get_cm_id())
                tip.set_input("<TestInstances>" + (element.text if element.text is not None else '') + ''.join(
                    etree.tostring(child, pretty_print=False, method='c14n') for child in element if
                    child.tag == "TestInstance") + "</TestInstances>")
                tis = tip.parse()
                if tis:
                    try:
                        for ti in tis:
                            tc.appendTestInstance(ti)
                    except Exception as e:
                        raise TestCaseParsingException("Could not append TestInstance " + str(e))
                else:
                    raise TestCaseParsingException("Could not parse TestInstance")
                result.append(tc)
        else:
            raise TestCaseParsingException("Element is not a TestCase tag")
        return result
