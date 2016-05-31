#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of cumulus-testagent.
# https://github.com/patriziotufarolo/cumulus-testagent

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>

from lxml import etree


class Parser(object):
    def __init__(self):
        self.__input = ""

    def set_input(self, parser_input):
        self.__input = parser_input

    def get_input(self):
        return self.__input

    def set_probe(self, parser_input):
        self.__probe = parser_input

    def get_probe(self):
        return self.__probe

    def set_cm_id(self, parser_input):
        self.__cm_id = parser_input

    def get_cm_id(self):
        return self.__cm_id

    def parse(self):
        pass
