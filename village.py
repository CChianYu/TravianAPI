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
        self.buildings = {}

        self.RH = handler.RequestsHandler()

    def updateAll(self):

        self.updateBuildings()

    def updateBuildings(self):

        for buildID in range(18, 20):

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
                self.postDebug(self.updateBuildings, str(buildID)+' is empty.')
                self.buildings[buildID] = {'name':'empty', 'canBuild':[]}
                
                for i in range(1, 4):

                    if u'即將可' in text:
                        text = parse.getStrBetween(text, '', u'即將可')
                    
                    while 'Wrapper' in text:
                        name = parse.getStrBetween(text, 'h2>', '</h2')
                        text = parse.getStrBetween(text, 'Wrapper', '')
                        #print(name)
                        if name not in self.buildings[buildID]['canBuild']:
                            self.buildings[buildID]['canBuild'].append(name)

                    if i == 3 :
                        break
                    getpage = BaseHttpAction.BaseHttpAction()
                    params = {'id':str(buildID), 'category':str(i+1)}
                    qID = self.RH.standby(self.updateBuildings, getpage, getpage.sendRequest, 'GET', 'build.php', params, getpage.end)
                    
                    text = self.RH.queue[qID].result.text
                    text = parse.getStrBetween(text, 'nHeader">', 'contentFooter')
                
            else :
                name = parse.getStrBetween(text, '', '<span')
                level = parse.getStrBetween(text,  u'等級', '</')
                
                self.buildings[buildID] = {'name':name, 'level':level}

                self.postDebug(self.updateBuildings, name + level)
    
    def runBuildAction(self, buildID, buildName = None):

        b = build.BuildAction(self.villageID, buildID, buildName)
        b.setSession(self.RH.session)
        b.buildStart()
            

if __name__ == '__main__':

    vil = Village(8999)
    #vil.runBuildAction(8)
    vil.runBuildAction(19, '倉庫')
    '''
    vil.updateBuildings()
    for buildID in vil.buildings:
        if vil.buildings[buildID]['name'] != 'empty':
            print(buildID, vil.buildings[buildID]['name'], vil.buildings[buildID]['level'])
        else :
            print(buildID ,  ' can build:')
            for canbuild in vil.buildings[buildID]['canBuild']:
                print(canbuild)
    '''
