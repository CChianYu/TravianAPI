#v0.0.1
from login import *
from BaseHttpAction import *
from BaseWorkflow import *
from bs4 import BeautifulSoup
import requests

class BuildAction(loginAction):

    def __init__(self, villageID, buildID):
        
        super(BuildAction, self).__init__()
        self.villageID = villageID
        self.buildID   = buildID
        params = {}

    def buildStart(self):

        print('準備建造 ' + str(self.buildID))
        
        params = {'id' : str(self.buildID)}
        self.sendRequest('GET', 'build.php', params, self.buildAction1)

    def buildAction1(self, response):

        soup = BeautifulSoup(response.text)
        if u'低流量或手機版本' in response.text:
            print('At login page')##

        list = soup.find_all('button', class_='green build')
        if list == [] :
            self.end(self.TRY_AGAIN, response)
            return

        list = str(list)
        i = list.find('c=')
        j = list.find('; re')

        params = {}
        params['c'] = list[i+2:j-1]
        params['a'] = str(self.buildID)

        self.sendRequest('GET', 'dorf1.php', params, self.buildAction2)
        
    def buildAction2(self, response):

        text = response.text

        if u'完成時間於' in text:
            self.end(self.SUCCESS)
            print('建築成功')
        else:
            self.end(self.ERROR)
            print('建築失敗')

if __name__ == '__main__':
    b = BuildAction(8999, 4)
    b.buildStart()
