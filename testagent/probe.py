from __future__ import absolute_import

__author__ = 'Patrizio Tufarolo'
__email__ = 'patrizio.tufarolo@studenti.unimi.it'
'''
Project: testagent
Author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
Date: 21/04/15
'''

import traceback, logging
from testagent.services.WorkerService import WorkerService

class Probe(object):
    def __init__(self):
        self.testinstances = {}
        self.atomicOperations = []
        self.logger = None
        self.cc = WorkerService().CeleryConfiguration

    def appendAtomic(self, action, rollback):
        self.atomicOperations.append({"action": action, "rollback": rollback})
        return

    def appendAtomics(self):
        pass

    def setLogger(self, logger):
        self.logger = logger

    def run(self, celeryobj, current_testcase, all_testcases, testcase):
        logger = self.logger
        for testinstance in testcase.getTestInstances():
            testinstances_inputs = testinstance.getInputs()
            if testinstance.getOperation() not in self.testinstances:
                self.testinstances[testinstance.getOperation()] = {}
            for singleInput in testinstances_inputs:
                self.testinstances[testinstance.getOperation()][singleInput] = testinstances_inputs[singleInput]

        counter = 0
        previousOutput = None
        celeryobj.update_state(state='PROGRESS', meta={
            'current_testcase': current_testcase,
            'all_testcases': all_testcases,
            'current_operation': 0,
            'total_operations': 0,
        })
        try:
            total_operations = len(self.atomicOperations)
            print total_operations
            for operation in self.atomicOperations:
                celeryobj.update_state(state='PROGRESS', meta={
                    'current_testcase': current_testcase,
                    'all_testcases': all_testcases,
                    'current_operation': counter + 1,
                    'total_operations': total_operations,
                })
                newOutput = operation["action"](previousOutput)
                previousOutput = newOutput
                counter = counter + 1
            logger.info("Everything went fine.")
            finalResult = previousOutput
        except Exception as e:
            logger.error("Phase " + str(counter) + " got exception. Reverting probe's operations. Step back to " + str(
                counter - 1) + " Exception: " + repr(e))
            logger.error(traceback.format_exc())
            roll_total = counter
            celeryobj.update_state(state='ROLLBACK', meta={
                'current_testcase': current_testcase,
                'all_testcases': all_testcases,
                'current_operation': counter,
                'total_operations': roll_total,
            })
            counter -= 1
            try:
                rollbackPrevOut = previousOutput
                for rollback in xrange(counter, -1, -1):
                    celeryobj.update_state(state='ROLLBACK', meta={
                        'current_testcase': current_testcase,
                        'all_testcases': all_testcases,
                        'current_operation': counter,
                        'total_operations': roll_total,
                    })
                    rollbackPrevOut = self.atomicOperations[counter]["rollback"](rollbackPrevOut)
                    counter = counter - 1
            except Exception as e:
                logger.error("Exception in rollback")
                logger.error(traceback.format_exc())
            finalResult = False
        # result_to_send = str(celeryobj.request.id) + "#" + str(finalResult)
        # print result_to_send
        return finalResult
