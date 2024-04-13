import hou

class Geo:
    '''This is the base class to create the geo container along with the anchor, transform, color, normal, and output nodes for all geo and geo children'''
    def __init__(self, inName='foobar'):
        '''Initialize the geo object'''
        self.name = inName
        self.createGeo()
        self.createAnchor()
        self.createTransform()
        self.createColor()
        self.createNormal()
        self.createOutput()
        self.layout()

    def createGeo(self):
        '''Creating the geo container'''
        self.topNode = hou.node('/obj')
        self.container = self.topNode.createNode('geo', self.name)
        self.container.setDisplayFlag(False)

    def createAnchor(self):
        '''A null anchor node that accepts input geometry/operations to apply all the general nodes used in the geo class'''
        self.anchor = self.container.createNode('null', 'ANCHOR')

    def createTransform(self):
        '''Creating transform node'''
        self.transform = self.container.createNode('xform', 'TRANSFORM')
        self.transform.setInput(0, self.anchor)

    def createColor(self):
        '''Creating color node'''
        self.color = self.container.createNode('color', 'COLOR')
        self.color.setInput(0, self.transform)

    def createNormal(self):
        '''Creating normal node'''
        self.normal = self.container.createNode('normal', 'NORMAL')
        self.normal.setInput(0, self.color)

    def createOutput(self):
        '''Creating common output sequence for all geo and geo children'''
        self.output = self.container.createNode('output', f'{self.name}_OUTPUT')
        self.output.setInput(0, self.normal)
        self.output.setDisplayFlag(True)
        self.output.setRenderFlag(True)    

    def layout(self):
        '''Layout inside and outside the container'''
        self.container.layoutChildren()
        self.topNode.layoutChildren()

    def hookup(self, geometry=None):
        '''Hooking up the geo info to the anchor node'''
        if geometry:
            self.anchor.setInput(0, geometry)
        self.layout()

    def __str__(self):
        '''A string override to print the name of the geo object'''
        return f'{self.name}'

    def __setattr__(self, name, value):
        '''A setattr override to set the tranform, rotation, scale, and color of the geo object'''
        if name in ('t', 'r', 's') and isinstance(value, tuple):
            if name == 't':
                self.transform.parmTuple('t').set(value)
            elif name == 'r':
                self.transform.parmTuple('r').set(value)
            elif name == 's':
                self.transform.parmTuple('s').set(value)
        elif name == 'c' and isinstance(value, tuple):
            self.color.parmTuple('color').set(value)                  
        else:
            self.__dict__[name] = value