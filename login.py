#v0.0.3
from BaseHttpAction import BaseHttpAction
from bs4 import BeautifulSoup
import UserInfo

class loginAction(BaseHttpAction):

    def __init__(self):
        super(loginAction, self).__init__()
        self.username = UserInfo.username
        self.password = UserInfo.password

    def loginStart(self):

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

        self.sendRequest('POST', 'dorf1.php', params, self.checkLogin)

    def loginAction2(self, response):

        text = response.text
        res = self.checkLogin(response)
        
    def checkLogin(self, response, callback = None):

        text = response.text

        if u'帳號不存在' in text:
            print('帳號錯誤')
            self.end(self.ERROR)
            return False
        elif u'密碼錯誤' in text:
            print('密碼錯誤')
            self.end(self.ERROR)
            return False
        elif 'captcha' in text:
            print('需要圖形驗證')
            self.end(self.ERROR)
            return False
        elif u'低流量或手機版本' in text:
            print('重新登入')
            self.loginAction1(response)
            self.end(self.TRY_AGAIN)
            print('check stack () 重新登入')

            return True

        if 'stockBar' in text:
            print('Login Success!!')
            self.end(self.SUCCESS)
            return True
        else:
            print('未知錯誤')
            self.end(self.ERROR, response)
            return False

if __name__ == '__main__':
    act = loginAction()
    #print(isinstance(act, BaseHttpAction))
    act.loginStart()

