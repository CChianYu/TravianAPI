#v0.0.1
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
        self.sendRequest('Get', 'login.php', None, self.loginAction1, None)
        
        print(u'準備登入:' + self.username)

    def loginAction1(self, response):
        
        soup = BeautifulSoup(response.text)
        form = soup.find_all('input')

        if len(form) != 5:
            print(u'未打開登入頁')
        print(form)

if __name__ == '__main__':
    act = loginAction()
    print(isinstance(act, BaseHttpAction))
    act.start()
