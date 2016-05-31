#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of cumulus-testagent.
# https://github.com/patriziotufarolo/cumulus-testagent

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>

from testagent.structure.testinstance import TestInstance

class TestCase(object):

    def __init__(self, ident, description):
        self.__id = ident
        self.__description = description
        self.__testInstances = []

    def getId(self):
        return self.__id

    def getDescription(self):
        return self.__description

    def appendTestInstance(self, testinstance):
        if isinstance(testinstance, TestInstance):
            self.__testInstances.append(testinstance)
        else:
            raise Exception("Argument testinstance is not a TestInstance")

    def getTestInstances(self):
        return self.__testInstances

    def run(self, probe):
        probe.run()
