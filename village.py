import handler
import build
import BaseHttpAction

class Village(BaseHttpAction.BaseHttpAction):

    def __init__(self, villageID):

        super(loadVillage, self).__init__()

        self.villageID = villageID
        self.buildings = []

    def updateAll(self):

        self.updateBuildings()

    def updateBuildings(self):

        for buildID in range(1, 2):

