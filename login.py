from BaseWorkflow import *
from BaseHttpAction import sendRequest
from bs4 import BeautifulSoup
import UserInfo

class loginAction(BaseHttpAction):

    def __init__(self):
        self.username = UserInfo.username
        self.password = UserInfo.password

    def start(self):
        
        sendRequest('Get', 'login.php', None, None, self.loginAction1)
        
        print(u'準備登入:' + self.username)

    def loginAction1(self, response):
        
        soup = BeautifulSoup(response.text)
        form = soup.find('input')

        if form.len != 5:
            print(u'未打開登入頁')
        print(form)
