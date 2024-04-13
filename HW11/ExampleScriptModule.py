import hou
from TubeModule import Tube
from BoxModule import Box

def main():
    '''Main function to create the objects and perform the boolean operations as required by the assignment.'''
    # in the python shell, run the following:
    # from ExampleScriptModule import main
    myBox = Box('myBox')

    myTube = Tube('myTube')
    myTube.t = (0, 0.5, 0)
    myTube.r = (90, 0, 0)
    myTube.s = (.5, 1, .5)

    but = myBox + myTube

    myBox2 = Box('myBox2')

    myBox3 = Box('myBox3')
    myBox3.t = (0, 0.5, 0.5)
    myBox3.r = (45, 0, 0)
    myBox3.s = (1, 1.414, 2)

    myBox4 = myBox2 - myBox3

    myTube2 = Tube('myTube2')
    myTube2.r = (90, 0, 0)
    myTube2.s = (.25,2, .25)

    wst = myBox4 - myTube2
    wst.t = (0, 0.5, 0.5)

    final = but&wst    
    final.c = (1, .8, .2)
    final.container.setDisplayFlag(True)

main()

# For SideFX to debug
# myBox = Box('myBox')
# myTube = Tube('myTube')
# myTube.t = (0, 2, 0)
# myTube.r = (0, 0, 45)
# myTube.s = (2.5, 2.5, 2.5)
# myTube.c = (1, 0, 0)
# myBox.t = (0, 2, 0)
# myBox.r = (0, 0, 45)
# myBox.s = (2.5, 2.5, 2.5)
# myBox.c = (1, 0, 0)
# union_test = myBox + myTube
# u2 = union_test -myTube