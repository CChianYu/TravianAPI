#v0.0.1
from login import *
from BaseHttpAction import *
from BaseWorkflow import *
from bs4 import BeautifulSoup
import requests

class BuildAction(BaseHttpAction):

    def __init__(self, villageID, buildID):
        
        super(BuildAction, self).__init__()
        self.villageID = villageID
        self.buildID   = buildID

    def buildStart(self):

        print('準備建造 ' + str(self.buildID))
        
        params = {'id' : str(self.buildID)}
        self.sendRequest('GET', 'build.php', params, self.buildAction1)

    def buildAction1(self, response):

        soup = BeautifulSoup(response.text)
        list = soup.find_all('button', class_='green build')
        self.postDebug(self.buildAction1, str(list))
        if u'低流量或手機版本' in response.text:
            print('At login page')
        self.pause()
        
        check = loginAction.checkLogin(self, response)
        if check == False:
            #BuildAction.start(self)
            self.end(self.TRY_AGAIN)
            return

        soup = BeautifulSoup(response.text)
        list = soup.find_all('button', class_='green build')

        self.postDebug(self.buildAction1, str(list))

if __name__ == '__main__':
    b = BuildAction(8999, 1)
    b.buildStart()
