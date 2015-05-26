import handler
import build
import BaseHttpAction
import handler
import parse
from bs4 import BeautifulSoup

class Village(BaseHttpAction.BaseHttpAction): # Village might inherent class Account

    def __init__(self, villageID):

        super(Village, self).__init__()

        self.villageID = villageID
        self.buildings = []

        self.RH = handler.RequestsHandler()

    def updateAll(self):

        self.updateBuildings()

    def updateBuildings(self):

        for buildID in range(38, 41):

            getpage = BaseHttpAction.BaseHttpAction()
            params = {'id':str(buildID)}
            
            qID = self.RH.standby(self.updateBuildings, getpage, getpage.sendRequest, 'GET', 'build.php', params, getpage.end)

            print(self.RH.queue[qID].status)
            print(self.RH.queue[qID].result)

            text = self.RH.queue[qID].result.text
            soup = BeautifulSoup(text)
            text = parse.getStrBetween(text, 'nHeader">', u'contentFooter') # find('titleInHeader')
            #print(text)

            if u'建造新的建築物' in text:
                for i in range(1, 4):
                    
                    while 'Wrapper' in text:
                        name = parse.getStrBetween(text, 'h2>', '</h2')
                        text = parse.getStrBetween(text, 'Wrapper', '')
                        print(name)

                    if i == 3 :
                        break
                    getpage = BaseHttpAction.BaseHttpAction()
                    params = {'id':str(buildID), 'category':str(i+1)}
                    qID = self.RH.standby(self.updateBuildings, getpage, getpage.sendRequest, 'GET', 'build.php', params, getpage.end)
                    
                    text = self.RH.queue[qID].result.text
                    text = parse.getStrBetween(text, 'nHeader">', '/span')

            else :
                name = parse.getStrBetween(text, '', '<span')
                level = parse.getStrBetween(text,  u'等級', '</')
                print(name, level)
            

if __name__ == '__main__':

    vil = Village(8999)
    vil.updateBuildings()
