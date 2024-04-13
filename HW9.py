import random

geo_types = [
    'box', 'sphere', 'tube', 'torus',
    'testgeometry_crag', 'testgeometry_rubbertoy',
    'testgeometry_pighead', 'testgeometry_shaderball',
    'testgeometry_squab', 'testgeometry_tommy'
]

selected_geo_types = []

def generate_army_of_darkness(base, level):
    num_soldiers = (base ** 3) ** (level - 1)
    geo = hou.node('/obj').createNode('geo', 'ArmyOfDarkness')

    #Spacing bw each soldier and unit
    spacing_soldier = 5
    spacing_unit = base * spacing_soldier
    
    last_node = None

    # Looping through each army unit
    for unit_index in range(num_soldiers // (base ** 3)):        
        # unique color for each unit
        rand_color = (random.random(), random.random(), random.random())
        
        global selected_geo_types
        soldier_type = random.choice(selected_geo_types)
        print(soldier_type)
        
        # center point of each unit based on their index
        x_unit = (unit_index % level) * spacing_unit
        z_unit = ((unit_index // level) % level) * spacing_unit
        y_unit = (unit_index // (level ** 2)) * spacing_unit
        
        # Looping through soldier for each unit
        for soldier_index in range(base ** 3):
            # center point of each solider based on its index
            x_soldier = x_unit + (soldier_index % base) * spacing_soldier
            z_soldier = z_unit + ((soldier_index // base) % base) * spacing_soldier
            y_soldier = y_unit + (soldier_index // (base ** 2)) * spacing_soldier

            rand_rot = (random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360))       

            soldier = geo.createNode(soldier_type, 'Soldier_{}_{}'.format(unit_index, soldier_index))
            
            color_node = geo.createNode('color', 'Color_{}_{}'.format(unit_index, soldier_index))
            color_node.setInput(0, soldier)
            color_node.parmTuple('color').set(rand_color)

            transform_node = geo.createNode('xform', 'Transform_{}_{}'.format(unit_index, soldier_index))
            transform_node.setInput(0, color_node)
            transform_node.parmTuple('r').set(rand_rot)
            transform_node.parmTuple('t').set((x_soldier, y_soldier, z_soldier))

            # creating last node to display
            if last_node is None:
                last_node = transform_node
            else:                
                merge_node = geo.createNode('merge')
                merge_node.setInput(0, last_node)
                merge_node.setInput(1, transform_node)
                last_node = merge_node

    # group_node = geo.createNode('groupcreate', 'Soldier_Group')
    # group_node.setInput(0, last_node)
    # group_node.parm('groupname').set('soldiers')
    # group_node.parm('grouptype').set(1)  # Set to 'Points'

    last_node.setDisplayFlag(True)

def main():
    base = int(hou.ui.readInput("Base:")[1])
    level = int(hou.ui.readInput("Level:")[1])    
        
    global geo_types
    
    choices = hou.ui.selectFromList(geo_types, exclusive=False, title="Ctrl select different geometry types:",
                                    column_header="Ctrl select different geometry types:", num_visible_rows=6)
    if not choices:
        hou.ui.displayMessage("Please select the geometries")
        return
        
    global selected_geo_types    
    
    selected_geo_types = [geo_types[i] for i in choices]
    print(selected_geo_types)
    
    generate_army_of_darkness(base, level)

main()