import hou
from CSGModule import CSG

class Tube(CSG):
    '''Class to create a tube object'''
    def __init__(self, inName = 'tube'):
        '''Initialize the tube object'''
        super().__init__(inName)
        self.createTube()

    def createTube(self):
        '''Create the tube, change it to polygon type, enable end caps, and connect it to the anchor node'''
        self.tube = self.container.createNode('tube', f'{self.name}')
        self.tube.parm('type').set(1)
        self.tube.parm('cap').set(1)
        self.hookup(self.tube)