from enum import Enum, auto

# Declaring the parent container node
parent_node = hou.node('/obj').createNode('geo', 'CSGContainer')

def create_label(parent, label_text, position):
    '''
    This function creates a label for each CSG operation result to be displayed below it.
    '''
    label_node = parent.createNode('font', node_name = f'label_{label_text}')
    label_node.parm('text').set(label_text)
    label_node.parmTuple('t').set(position)
    label_node.parm('fontsize').set(0.25)
    return label_node

class shape(Enum):
    '''
    An enumeration representing various types of geometric shapes that the CSG object can be.
    '''
    # auto() is used to automatically assign a value to each shape from 1 to n
    box = auto()
    sphere = auto()
    tube = auto()
    torus = auto()
    roberto = auto()
    crag = auto()
    pig = auto()
    shaderBall = auto()
    squab = auto()
    tommy = auto()

    def shape_string(self):
        '''
        This function maps the shape enumeration to the corresponding string name of the geometry node.
        '''
        shape_str_map = {
            shape.box: 'box',
            shape.sphere: 'sphere',
            shape.tube: 'tube',
            shape.torus: 'torus',
            shape.roberto: 'testgeometry_rubbertoy',
            shape.crag: 'testgeometry_crag',
            shape.pig: 'testgeometry_pighead',
            shape.shaderBall: 'testgeometry_shaderball',
            shape.squab: 'testgeometry_squab',
            shape.tommy: 'testgeometry_tommy'
        }
        return shape_str_map.get(self)
    
class CSG:
    '''
    This class represents a CSG object.
    It consists of various geometric shapes that can be combined using boolean operations.
    '''
    def __init__ (self, name, shape_type):
        '''
        The shapes are initialized with a name and a shape type.
        A node represting the shape is created and stored in the node attribute.
        Its name is stored in the name attribute.
        '''
        if not isinstance(shape_type, shape):
            raise TypeError('shape_type must be an instance of shape')
                
        shape_str = shape_type.shape_string()
        self.node = parent_node.createNode(shape_str, node_name = name)
        self.name = name

    # A list to store the CSG operation results
    objects = []    

    def csg_nodes_setup(self, operation, other, subtract_choice=None, label_text=''):
        '''
        This is a base function to create the boolean and normal nodes for the CSG operation to be used by various overload operators later.
        It merges the boolean node with the label of the operation result and stores it in the objects list.
        '''
        # Creating the boolean node
        bool_node = self.node.createOutputNode('boolean')
        bool_node.parm('booleanop').set(operation)

        # Setting the subtractchoices parameter to (B-A) or (A-B) if the operation is subtraction
        if operation == 2 and subtract_choice is not None:
            bool_node.parm('subtractchoices').set(subtract_choice)
        
        # Creating references to objects rather than using their instances directly
        merge_self = parent_node.createNode('object_merge', node_name=f'merge_{self.name}')
        merge_self.parm('objpath1').set(self.node.path())
        merge_other = parent_node.createNode('object_merge', node_name=f'merge_{other.name}')
        merge_other.parm('objpath1').set(other.node.path())

        # Connect object merge nodes to boolean node
        bool_node.setInput(0, merge_self)
        bool_node.setInput(1, merge_other)

        normal_node = bool_node.createOutputNode('normal')

        # Merging the label node
        label_node = create_label(parent_node, label_text, (0, -1, 0))
        merge_node = normal_node.createOutputNode('merge')
        merge_node.setInput(1, label_node)

        CSG.objects.append((label_text, merge_node)) 

    def __invert__(self):
        '''
        This function overloads the ~ operator to perform an inversion operation on a CSG object.
        Unlike other operations, this operation only requires one CSG object and creates a negative node using a sphere and subtracts the CSG object from it.
        '''
        other = CSG('negative', shape.sphere)
        self.csg_nodes_setup(2, other, subtract_choice=1, label_text = f'Invert_{self.name}')

    def __add__(self, other):
        '''
        This function overloads the + operator to perform a union operation between two CSG objects.
        '''
        self.csg_nodes_setup(0, other, label_text=f'Union_{self.name}_{other.name}')
    
    def __sub__(self, other):
        '''
        This function overloads the - operator to perform a subtraction operation between two CSG objects.
        '''
        self.csg_nodes_setup(2, other, subtract_choice=0, label_text=f'Subtract_{self.name}_{other.name}') 
    
    def __and__(self, other):
        '''
        This function overloads the & operator to perform an intersection operation between two CSG objects.
        '''
        self.csg_nodes_setup(1, other, label_text=f'Intersect_{self.name}_{other.name}')
    
    def __str__(self):
        '''
        This function returns a string representation of the CSG object.
        '''
        return f'CSG Object: {self.name}, Type: {self.node.type().name()}'
    
    def __setattr__(self, name, value):
        '''
        This function overloads the __setattr__ function to set the primitive type to be a Polygon if the shape is a sphere or a tube.
        '''
        if name == 'node' and (value.type().name() == 'sphere' or value.type().name() == 'tube'):
            value.parm('type').set(1)
        super(CSG, self).__setattr__(name, value)
    
    def arrange_nodes():
        '''
        This function arranges the nodes in the scene view.
        '''
        merge_node = parent_node.createNode('merge', 'final_merge')
        x_offset = 0

        # Offset the nodes representing each operation in the x direction and connect them to the merge node to display them together
        for label_text, op_node in CSG.objects:
            xform_node = op_node.createOutputNode('xform', node_name=f'transform_{label_text}')
            xform_node.parmTuple('t').set((x_offset, 0, 0))
            x_offset += 2

            merge_node.setNextInput(xform_node)

        merge_node.setDisplayFlag(True)
        return merge_node

def main(): 
    '''
    This function creates an example of various CSG objects and performs various operations on them.
    ''' 
    a = CSG('a', shape.box)
    b = CSG('b', shape.sphere)
    c = CSG('c', shape.tube)
    d= CSG('d', shape.torus)
    e = CSG('e', shape.roberto)
    f = CSG('f', shape.crag)
    g = CSG('g', shape.pig)
    h = CSG('h', shape.shaderBall)
    i = CSG('i', shape.squab)
    j = CSG('j', shape.tommy)    

    test1 = a + j
    test2 = i - d
    test3 = g & a
    test4 =  ~e
    test5 = h + j
    test6 = j - a
    test7 = b & e
    test8 = ~d
    test9 = e + a
    test10 = g - h
    test11 = i & j
    test12 = ~g

    # Arrange the nodes in the scene view
    CSG.arrange_nodes()

main()
