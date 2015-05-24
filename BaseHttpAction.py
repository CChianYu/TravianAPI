#v0.0.3
from BaseWorkflow import *
import UserInfo
import requests

class BaseHttpAction(BaseWorkflow):

    villageID = None
    serverURL = ''
    session = None

    def __init__(self, ID = None):

        super(BaseHttpAction, self).__init__()
        
        self.villageID = ID
        self.serverURL = 'http://' + UserInfo.serverURL + '/'
        self.session = requests.Session()

    def sendRequest(self, case, url, param, nextStep,  refer = None):

        if self.villageID != None:
            url += '?' if '?' not in url else '&'
            url += 'newdid=' + str(self.villageID)

        headers = self.setHeaders(refer)
        url = self.serverURL + url
        res = None
       
        print('url: ' + url)
        #print('Get' if case == 'Get' else 'Post')
        #self.postDebug('param: ' + ('None' if param is None else str(param)))
        #print('headers: ' + str(headers))
        
        if case == 'GET':
            res = self.session.get(url, params = param, headers = headers)
        else:
            res = self.session.post(url, data = param, headers = headers)

        nextStep(res) #接收response 執行下一步

    def setHeaders(self, refer):
        headers = {'content-type':'application/x-www-form-urlencoded', 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'}
        if refer:
            headers['Referer'] = refer
        return headers
