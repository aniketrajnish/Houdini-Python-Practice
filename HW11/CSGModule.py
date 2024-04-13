import hou
from GeoModule import Geo

class CSG(Geo):
    def __init__(self, inName='CSG'):
        '''Intializing the CSG object'''
        super().__init__(inName)

    def addBooleanOperation(self, operation, other):
        '''Base function to add boolean operations to the CSG objects'''

        # Assigning the name of operation on the basis of the operation number to be used in the name of the CSG object
        operation_symbols = { 0: 'Union', 1: 'Intersect', 2: 'Subtract'}
        operation_symbol = operation_symbols.get(operation, operation)       
        result_csg = CSG(f'{self.name}{operation_symbol}{other.name}')
        
        # Creating the object merge nodes to merge the two Geo objects
        mergeA = result_csg.container.createNode('object_merge', f'merge_{self.name}')
        mergeA.parm('objpath1').set(self.output.path())
        mergeB = result_csg.container.createNode('object_merge', f'merge_{other.name}')
        mergeB.parm('objpath1').set(other.output.path())

        # Creating the boolean node to perform the boolean operation, connecting the two merge nodes to it, and hooking it up to the anchor node  
        boolean_node = result_csg.container.createNode('boolean', f'boolean_{operation}')
        boolean_node.parm('booleanop').set(operation)
        boolean_node.setInput(0, mergeA)
        boolean_node.setInput(1, mergeB)
        result_csg.hookup(boolean_node)
        self.layout()        
        return result_csg  

    def __add__(self, other):
        '''Overriding the add operator to perform the union operation'''
        return self.addBooleanOperation(0, other)  
    def __sub__(self, other):
        '''Overriding the subtract operator to perform the subtract operation'''
        return self.addBooleanOperation(2, other)  
    def __and__(self, other):
        '''Overriding the and operator to perform the intersect operation'''
        return self.addBooleanOperation(1, other)