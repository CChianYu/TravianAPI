class BaseWorkflow:

    def __init__(self):
        self.whoCall = None    # An object
        self.afterDone = None  # A function
        self.status = None

    def run(self, whoCall, afterDone):
        self.whoCall = whoCall
        self.afterDone = afterDone

    def end(self, status = None):
        self.status = status
        self.afterDone()
