#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of cumulus-testagent.
# https://github.com/patriziotufarolo/cumulus-testagent

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>

from testagent.structure.testcase import TestCase

class Collector(object):

    def __init__(self, ident, cmid, tot):
        self.__id = ident
        self.__cmId = cmid
        self.__tot = tot
        self.__testcases = []

    def getId(self):
        return self.__id

    def getCmId(self):
        return self.__cmId

    def getTot(self):
        return self.__tot

    def getTestcases(self):
        return self.__testcases

    def appendTestCase(self, testcase):
        if isinstance(testcase, TestCase):
            self.__testcases.append(testcase)
        else:
            raise Exception("Argument testcase is not a TestCase")
