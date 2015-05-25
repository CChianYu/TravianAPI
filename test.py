from BaseWorkflow import *

class test(BaseWorkflow):
    
    def __init__(self):
        super(BaseWorkflow, self).__init__()
        self.name = ''
        self.val = 0

    def setName(self, name):
        self.name = name

    def __str__(self):
        return str(type(self))

    def result(self):
        print(self)

if __name__=='__main__':
    
    t1 = test()
    t2 = test()
    t1.setName('t1')
    t2.setName('t2')
    t1.result()
    t2.result()
    t1.run(t1, t1.result)
    t1.end()
