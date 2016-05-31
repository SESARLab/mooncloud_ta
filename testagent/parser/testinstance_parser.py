#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of cumulus-testagent.
# https://github.com/patriziotufarolo/cumulus-testagent

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>

from lxml import etree

from testagent.parser import Parser

from testagent.parser.exceptions import TestInstanceParsingException
from testagent.structure import TestInstance
from testagent.selfassessment import SelfAssessment


class TestInstanceParser(Parser):
    def parse(self):
        try:
            root = etree.fromstring(self.get_input())
        except etree.XMLSyntaxError as e:
            raise TestInstanceParsingException(e)

        if root.tag.lower() == "testinstances":
            result = []
            for ti in root:
                # I am only handling Inputs for now
                if ti.tag.lower() == "testinstance":
                    ti_id = ti.get("Operation")
                    ti_obj = TestInstance(ti_id)

                    for elements in ti:
                        if elements.tag == "Input":
                            for inputitem in elements:
                                input_key = inputitem.get("key")
                                print("CHIAVE:" + input_key)
                                try:
                                    input_value = inputitem.get("value") 
                                except:
                                    pass
                                print("VALORE:" , input_value or "")
                                try:
                                    if input_value is None:# or input_value == "":
                                        print("cientro")
                                        input_value = \
                                            SelfAssessment().get_self_assessment(self.get_probe(), self.get_cm_id())[ti_id][input_key]
                                        pass
                                except:
                                    raise TestInstanceParsingException(
                                        "No value provided for key " + input_key + ". Check the xml input or the self assessment configuration file.")

                                try:
                                    ti_obj.appendInput(input_key, input_value)
                                except:
                                    raise TestInstanceParsingException("Malformed input item")
                    result.append(ti_obj)
                else:
                    raise TestInstanceParsingException("Element is not TestInstance")
            return result
        else:
            raise TestInstanceParsingException("Element is not TestInstances")
