__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'

from testagent.probe import Probe
from time import sleep


class EmptyProbe(Probe):
    def ciao0(self, inputs):
        import os, datetime
        # print 'process id:', os.getpid()
        # print 'time:' +str(datetime.datetime.now())
        self.logger.info('process id:' + str(os.getpid()) + ' - time:' + str(datetime.datetime.now()))
        return True

    def ciao0r (self, inputs):
        return

    def appendAtomics(self):
        self.appendAtomic(self.ciao0, self.ciao0r)

probe = EmptyProbe
