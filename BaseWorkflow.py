#v0.0.0
import os
class BaseWorkflow:
    SUCCESS = 'SUCCESS'
    ERROR   = 'ERROR'
    TRY_AGAIN = 'TRY_AGAIN'
    
    whoCall = None
    afterDone = None
    status = None
    DEBUG = True

    def __init__(self):
        self.whoCall = None    # An object
        self.afterDone = None  # A function
        self.status = None

    def run(self, whoCall, afterDone):
        self.whoCall = whoCall
        self.afterDone = afterDone

    def end(self, *argv):

        response = None
        if len(argv) > 1:    # 3 kinds of situation: argv=(['', response], [''], ['response'])
            self.status = argv[0]
            response    = argv[1]
        else:
            if type(argv[0]) == type(str()):
                self.status = argv[0]
            else :
                self.status = self.SUCCESS
                response    = argv[0]

        if self.afterDone is not None:
            self.afterDone(response)

    def postDebug(self, whocall, msg):
        if self.DEBUG:
            s = str(whocall).find('method')
            e = str(whocall).find('of')
            print('DEBUG: '+str(whocall)[s:e] + msg)

    def pause(self):
        if self.DEBUG:
            input()
