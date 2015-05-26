import handler
import build
import BaseHttpAction
import handler

class Village(BaseHttpAction.BaseHttpAction): # Village might inherent class Account

    def __init__(self, villageID):

        super(Village, self).__init__()

        self.villageID = villageID
        self.buildings = []

        self.RH = handler.RequestsHandler()

    def updateAll(self):

        self.updateBuildings()

    def updateBuildings(self):

        for buildID in range(1, 2):

            getpage = BaseHttpAction.BaseHttpAction()
            params = {'id':str(buildID)}
            
            qID = self.RH.standby(self.updateBuildings, getpage, getpage.sendRequest, 'GET', 'build.php', params, getpage.end)

            print(self.RH.queue[qID].status)
            print(self.RH.queue[qID].result[0])
            
if __name__ == '__main__':

    vil = Village(8999)
    vil.updateBuildings()
