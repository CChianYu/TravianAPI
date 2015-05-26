import BaseHttpAction
import BaseWorkflow
import requests
import login
import build

class RequestsHandler(BaseHttpAction.BaseHttpAction):

    def __init__(self):

        super(RequestsHandler, self).__init__()

        self.session = requests.Session()
        self.queue = []
        self.qnow = 0
        self.canGo = True

    def standby(self, whoCall, obj, function, *argv):

        nex = work(whoCall, self.done, obj, function, *argv)

        self.queue.append(nex)

        if self.canGo == True:
            self.go()

        return len(self.queue) - 1  #return queID
            

    def go(self):

        self.canGo = False

        now = self.queue[self.qnow]

        now.apply(self.session)

    def done(self, response):
        
        if response != None:   

            check = login.loginAction()
            check.setSession(self.session)
            check.checkLogin(response)
            #self.postDebug(self.done, check.status)
            if check.status == self.TRY_AGAIN:
                self.queue[self.qnow].status = self.TRY_AGAIN
                self.queue[self.qnow].result = response
            else:
                self.queue[self.qnow].status = self.ERROR
                self.queue[self.qnow].result = response
        else :
            self.queue[self.qnow].status = self.SUCCESS
            self.queue[self.qnow].result = response

        self.nextwork()

    def nextwork(self):

        self.qnow += 1

        if self.qnow < len(self.queue):
            self.go()
        else:
            self.canGo = True

class work(BaseWorkflow.BaseWorkflow):

    def __init__(self, whoCall, callback, obj, function, *arguments):
        
        super(work, self).__init__()

        self.whoCall = whoCall
        self.callback = callback
        self.obj = obj
        self.function = function
        self.arguments = arguments
        self.status = None
        self.result = None

    def apply(self, session):

        obj  = self.obj
        func = self.function
        arg  = self.arguments

        obj.setSession(session)
        #self.postDebug(self.apply, str(session)+str(obj.session))
        #self.postDebug(self.apply, str(session.cookies))

        obj.run(self.whoCall, self.callback)
        func(*arg)
        
if __name__ == '__main__':

    god = RequestsHandler()
    build = build.BuildAction(8999, 6)
    checkID = god.standby(build, build, build.buildStart)
    print(god.queue[checkID].status)

    #god.postDebug(god, 'handler'+str(god.session.cookies))
    if god.queue[checkID].status == god.TRY_AGAIN:
        checkID = god.standby(build, build, build.buildStart)
        #god.pause()
    print(god.queue[checkID].status)
    #print(god.queue[checkID].result[1].text)
