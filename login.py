#v0.0.2
from BaseHttpAction import *
from bs4 import BeautifulSoup
import UserInfo

class loginAction(BaseHttpAction):

    def __init__(self):
        super(loginAction, self).__init__()
        self.username = UserInfo.username
        self.password = UserInfo.password
        print('loginAction init')

    def start(self):

        print(u'準備登入:' + self.username)

        self.sendRequest('GET', 'login.php', None, self.loginAction1, None)

    def loginAction1(self, response):
        
        soup = BeautifulSoup(response.text)
        form = soup.find_all('input')

        if len(form) != 5:
            print(u'未打開登入頁')
        
        params = {}
        for tag in form:
            if tag['type'] == 'text':
                params[tag['name']] = self.username
            elif tag['type'] == 'password':
                params[tag['name']] = self.password
            elif tag['name'] == 'w':
                params[tag['name']] = '1280:720'
            else :
                params[tag['name']] = tag['value']
        self.postDebug(str(params))
        self.sendRequest('POST', 'dorf1.php', params, self.loginAction2)

    def loginAction2(self, response):
        soup = BeautifulSoup(response.text)
        form = soup.find_all('input')
        list = soup.find_all('li', class_='stockBarButton')

        for tag in form:
            if u'帳號不存在' in str(tag):
                print('帳號錯誤')
                self.end('ERROR')
                return
            elif u'密碼錯誤' in str(tag):
                print('密碼錯誤')
                self.end('ERROR')
                return
            elif 'captcha' in str(tag):
                print('需要圖形驗證')
                self.end('ERROR')
                return
        if len(list) > 0 :
            print('登入成功')
            self.end('SUCCESS')
        self.postDebug(str(form))
        self.postDebug(str(list))

if __name__ == '__main__':
    act = loginAction()
    print(isinstance(act, BaseHttpAction))
    act.start()
