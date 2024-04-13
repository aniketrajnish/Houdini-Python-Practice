import random
from PySide2 import QtWidgets, QtGui, QtCore

class ScaleDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ScaleDialog, self).__init__(parent)

        self.init_ui()

    def init_ui(self):
        vbox = QtWidgets.QVBoxLayout(self)

        self.scale_label = QtWidgets.QLabel("Enter scale of the point clouds (between 0.1 and 10.0):", self)
        vbox.addWidget(self.scale_label)

        self.scale_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.scale_slider.setMinimum(1)  
        self.scale_slider.setMaximum(100.0)  
        self.scale_slider.setValue(10.0) 
        self.scale_slider.valueChanged.connect(self.update_scale_label)
        vbox.addWidget(self.scale_slider)

        self.scale_value_label = QtWidgets.QLabel("1.0", self)
        vbox.addWidget(self.scale_value_label)

        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        vbox.addWidget(buttons)

    def update_scale_label(self, value):
        scale = value / 10.0
        self.scale_value_label.setText(str(scale))

    def scale_value(self):
        return self.scale_slider.value() / 5000.0      

class NumberInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NumberInputDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        vbox = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Select number of point clouds (between 1 and 1,000,000):", self)
        vbox.addWidget(self.label)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(1000000)
        self.slider.setValue(50000)
        self.slider.valueChanged.connect(self.update_label)
        vbox.addWidget(self.slider)

        self.value_label = QtWidgets.QLabel("50000", self)
        vbox.addWidget(self.value_label)

        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        vbox.addWidget(buttons)

    def update_label(self, value):
        self.value_label.setText(str(value))

    def number_value(self):
        return self.slider.value()

# Method to extract a specific type of child from 
def extractChild(parent, childType):
    listOfChildrens = parent.children()
    for node in listOfChildrens:
        if node.type().name() == childType:
            return node       
            
# Declaring the parent           
parentNode = hou.node('/obj')

# Asking to choose the shape
shapes = ["tube", "torus", "sphere", "box"]
shape_choice = hou.ui.selectFromList(shapes, title="Select Point Cloud Shape", column_header="Shapes")
if not shape_choice:
    raise Exception("Please select a shape")
chosen_shape = shapes[shape_choice[0]]

# Asking to choose the scale
scale_dialog = ScaleDialog()
if scale_dialog.exec_():
    chosen_scale = scale_dialog.scale_value()
else:
    raise Exception("Please choose a scale")
    
# Asking the path of the geometry node to build the point clouds around in Houdini
model_path = hou.ui.selectNode(title="Select Geometry Node to build point clouds around", node_type_filter=hou.nodeTypeFilter.Sop)
if not model_path:
    raise Exception("Please select a geometry node first")

selected_geo = hou.node(model_path)
last_node_in_geo = selected_geo.children()[-1] 

# Connecting the last node of the selected geometry node (the mesh file) to the attribfrommap node to get its UV and color info
attrib_from_map = selected_geo.createNode("attribfrommap", "Attribute_from_Map")
attrib_from_map.setInput(0, last_node_in_geo)

# Creating the scatter nodes
scatter_node = selected_geo.createNode("scatter", "Scattered_Points")
scatter_node.setInput(0, attrib_from_map)

# Asking the user for the number of point clouds
number_input_dialog = NumberInputDialog()
if number_input_dialog.exec_():
    num_points = number_input_dialog.number_value()
else:
    raise Exception("Please choose the number of point clouds:")

scatter_node.parm("npts").set(num_points)

# Getting the basemap texture of the mesh to pass color information to the point clouds
material_node = extractChild(last_node_in_geo, 'matnet')
if not material_node:
    raise Exception("material node not found.")
    
basecolor_texture_parm = material_node.children()[0].parm("basecolor_texture")

if not basecolor_texture_parm:
    raise Exception("basecolor_texture parameter not found.")

texture_path = basecolor_texture_parm.eval()
attrib_from_map.parm("filename").set(texture_path)
attrib_from_map.parm("export_attribute").set("Cd")

# Creating one point cloud
shapeNode = selected_geo.createNode(chosen_shape, f"Shape_{chosen_shape}")
if chosen_shape == "tube":
    shapeNode.parm("rad1").set(chosen_scale)
    shapeNode.parm("rad2").set(chosen_scale)
    shapeNode.parm("height").set(chosen_scale)
else:
    shapeNode.parm("scale").set(chosen_scale)

# Creating copy node and to draw the point clouds at them
copy_node = selected_geo.createNode("copytopoints", "Copy_to_Points")
copy_node.setInput(0, shapeNode)
copy_node.setInput(1, scatter_node)  

# Tranferrring the color info to the point clouds
attrib_transfer = selected_geo.createNode("attribtransfer", "Transfer_Color")
attrib_transfer.setInput(0, copy_node)  
attrib_transfer.setInput(1, scatter_node)  
attrib_transfer.parm("pointattriblist").set("Cd") 

# Display the point clouds with the color info
attrib_transfer.setDisplayFlag(True)