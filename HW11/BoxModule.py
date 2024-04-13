import hou
from CSGModule import CSG

class Box(CSG):
    '''Class to create a box object'''
    def __init__(self, inName = 'box'):
        '''Initialize the box object'''
        super().__init__(inName)
        self.createBox()

    def createBox(self):
        '''Create the box and connect it to the anchor node'''
        self.box = self.container.createNode('box', f'{self.name}')
        self.hookup(self.box)