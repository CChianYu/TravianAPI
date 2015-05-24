#v0.0.3
from BaseWorkflow import *
import UserInfo
import requests

class BaseHttpAction(BaseWorkflow):

    villageID = None
    serverURL = ''
    cookies   = {}

    def __init__(self, ID = None):

        super(BaseHttpAction, self).__init__()
        
        self.villageID = ID
        self.serverURL = 'http://' + UserInfo.serverURL + '/'

    def sendRequest(self, case, url, param, nextStep,  refer = None):

        if self.villageID != None:
            url += '?' if '?' not in url else '&'
            url += 'newdid=' + str(self.villageID)

        headers = self.setHeaders(refer)
        url = self.serverURL + url
        res = None
        cookies = BaseHttpAction.cookies
        self.postDebug(self.sendRequest, 'Cookies: ' + str(cookies))
       
        print('url: ' + url)
        #print('Get' if case == 'Get' else 'Post')
        #self.postDebug('param: ' + ('None' if param is None else str(param)))
        #print('headers: ' + str(headers))
        
        if case == 'GET':
            res = requests.post(url, params = param, headers = headers, cookies = cookies)
        else:
            res = requests.post(url, data = param, headers = headers, cookies = cookies)

        self.updateCookies(res)

        self.checkSessid(res)

        nextStep(res) #接收response 執行下一步

        #req = requests.Request(method = case, url = url, params = param, headers = headers)
        #r = req.prepare()
        #res = requests.Session().send(r)
    def checkSessid(self, response):
        if 'sess_id' in str(response.cookies):
            sess_id = self.parseSessid(str(response.cookies))
            if len(sess_id) == 32:
                BaseHttpAction.cookies['sess_id'] = sess_id
                self.postDebug(self.checkSessid, 'Check Sess ID: ' + sess_id)

    def updateCookies(self, response):
        print('method updateCookies'+str(response.cookies))

    def setHeaders(self, refer):
        headers = {'content-type':'application/x-www-form-urlencoded', 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36'}
        if refer:
            headers['Referer'] = refer
        return headers

    def parseSessid(self, s):
        i = s.find('sess_id=')
        return s[i+8:i+40]
