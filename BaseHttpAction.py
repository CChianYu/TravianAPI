from BaseWorkflow import *
import UserInfo
import requests

class BaseHttpAction(BaseWorkflow):

    def __init__(self, villageID = None):

        super(BaseWorkflow, self).__init__()
        
        self.villageID = villageID
        self.serverURL = 'http://' + UserInfo.serverURL + '/'

    def sendRequest(self, case, url, param, refer = None, nextStep):

        if villageID:
            url += '?' if '?' not in url else '&'
            url += villageID

        headers = self.setHeaders(refer)
        url = self.serverURL + url
        res = None
       
        if case == 'Get':
            res = requests.get(url, param, headers)
        else:
            res = requests.post(url, param, headers)

        nextStep(res) #接收response 執行下一步

        print('url: ' + url)
        print('Get' if cas == 'Get' else 'Post')
        print('param:' + param)
        print('headers:' + headers)

    def setHeaders(self, refer):
        headers = {'content-type':'application/x-www-form-urlencoded', 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'}
        if refer:
            headers['Referer'] = refer
        return headers

