#v0.0.1
import BaseHttpAction
from bs4 import BeautifulSoup
import requests
import parse

class BuildAction(BaseHttpAction.BaseHttpAction):

    def __init__(self, villageID, buildID, buildName = None):
        
        super(BuildAction, self).__init__()
        self.villageID = villageID
        self.buildID   = buildID
        self.buildName = buildName
        params = {}

    def buildStart(self):

        print('準備建造 ' + str(self.buildID))
        
        params = {'id' : str(self.buildID)}
        self.sendRequest('GET', 'build.php', params, self.buildAction1)

    def buildAction1(self, response):

        list = response.text
        if u'低流量或手機版本' in list:
            print('At login page')##

        if 'green build' in list :
            self.end(self.TRY_AGAIN, response)
            return

        params = {}
        url = ''

        if u'新的建築' in list:
            list = parse.getStrBetween(list, u'新的建築', u'即將可')
            list = parse.getStrBetween(list, self.buildName, 'buildingWrapper')
            list = parse.getStrBetween(list, 'dorf2.php?', '\">')

            self.postDebug(self.buildAction1, list)

            a = parse.getStrBetween(list, 'a=', '&')
            c = parse.getStrBetween(list, 'c=', '\'; re')

            params['a'] = a
            params['c'] = c
            params['id'] = str(self.buildID)

            url = 'dorf2.php'
        else:
            if self.buildID <= 18:
                url = 'dorf1.php'
            else:
                url = 'dorf2.php'

            list = parse.getStrBetween(list, 'green build', '">')
            a = parse.getStrBetween(list, 'a=', '&')
            c = parse.getStrBetween(list, 'c=', '\'; re')

            params['c'] = c 
            params['a'] = a

            self.postDebug(self.buildAction1, list)

        self.sendRequest('GET', url, params, self.buildAction2)
        
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
    b = BuildAction(8999, 19, '倉庫')
    b.buildStart()
