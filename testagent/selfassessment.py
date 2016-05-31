__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'
'''
Project: testagent
Author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
Date: 21/04/15
'''

import ConfigParser
import codecs
from testagent.utils.Singleton import Singleton
from testagent.exceptions.SelfAssessmentException import SelfAssessmentException
class SelfAssessment(Singleton):
    cache = {}

    def configure(self, basedir):
        self.basedir = basedir if basedir[-1] == "/" else basedir + "/"
        super(SelfAssessment, self).configure()

    @Singleton._if_configured(SelfAssessmentException)
    def __load_self_assessment(self, probename, cmid):
        try:
            parser = ConfigParser.SafeConfigParser()
            parser.optionxform = str
            with codecs.open(self.basedir + cmid + "/" + probename + ".conf", 'r', encoding='utf-8') as f:
                parser.readfp(f)
        except ConfigParser.ParsingError as err:
            raise SelfAssessmentException("Could not parse Self Assessment file for probe " + probename)
        except IOError:
            raise SelfAssessmentException("Self Assessment file for probe " + probename + "does not exist")

        self.cache[cmid][probename] = {}
        for section in parser.sections():
            self.cache[cmid][probename][str(section)] = {}
            for key, value in parser.items(section):
                self.cache[cmid][probename][str(section)][str(key)] = str(value)
        return True

    @Singleton._if_configured(SelfAssessmentException)
    def get_self_assessment(self, probename, cm_id):
        try:
            try:
                if not isinstance(self.cache[cm_id], dict):
                    self.cache[cm_id] = {}
            except KeyError, e:
                self.cache[cm_id] = {}
            
            #print(self.cache)
            if isinstance(self.cache[cm_id][probename], dict):
                return self.cache[cm_id][probename]
            else:
                if self.__load_self_assessment(probename, cm_id):
                    return self.get_self_assessment(probename, cm_id)
        except:
            self.cache[cm_id][probename] = self.__load_self_assessment(probename, cm_id)
            return self.get_self_assessment(probename, cm_id)

    @Singleton._if_configured(SelfAssessmentException)
    def reload_cache_for_probe(self, probename, cmid):
        self.cache[cmid][probename] = self.__load_self_assessment(probename, cmid)
        return
