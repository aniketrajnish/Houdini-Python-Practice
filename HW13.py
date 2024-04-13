# Create a shelf tool, paste the following script and run it.

import json

def python_sop_script(file_path):
    '''
    This function is used to return the script for the Python SOP as a string.
    It is used to generate the Points and Polygons constituting the countries and assigning a unique color to each country.
    It handles both 'Polygon' and 'MultiPolygon' types of GeoJSON data.
    '''
    return '''
import json
import random
geo = hou.pwd().geometry()

geo.addAttrib(hou.attribType.Point, 'Cd', (0.0, 0.0, 0.0)) # Add color attribute to the points

with open('{}', 'r') as file:
    data = json.load(file) # Load the json data

for feature in data['features']:
    color = (random.random(), random.random(), random.random()) # Unique color for each country
    
    if feature['geometry']['type'] == 'Polygon':
        for coordinates in feature['geometry']['coordinates']: # Cycle through the coordinates, make a point for each coordinate and add it to vertex of the polygon making up the country         
            poly = geo.createPolygon()                
            
            for x,y in coordinates:  
                point = geo.createPoint()
                point.setPosition((-x, 0, y)) # Somehow the x coordinate is reversed in the JSON data, so reversed it back here
                point.setAttribValue('Cd', color)               
                poly.addVertex(point)

    # Handle 'MultiPolygon' type
    elif feature['geometry']['type'] == 'MultiPolygon':
        for polygon in feature['geometry']['coordinates']: # Cycle through each polygon in the MultiPolygon and perform the same steps as above, but for each polygon in the MultiPolygon the color is the same representing the same country
            for coordinates in polygon:
                poly = geo.createPolygon()

                for x, y in coordinates:  
                    point = geo.createPoint()
                    point.setPosition((-x, 0, y))     
                    point.setAttribValue('Cd', color)                
                    poly.addVertex(point)
    '''.format(file_path.replace('\\', '\\\\')) # Replaced to avoid errors

# Select the GeoJSON file, generate the Points and Polygons constituting the countries using a Python SOP by feeding the above script to it.
file_path = hou.ui.selectFile(title='Select the GeoJSON File', file_type=hou.fileType.Any, pattern='*.geojson')

if file_path:   
    geo_container = hou.node('/obj').createNode('geo', 'Countries')     
    python_sop = geo_container.createNode('python', 'Countries')    
    python_sop.parm('python').set(python_sop_script(file_path))