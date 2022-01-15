import random

from room import *
import copy


class Robber:
    def __init__(self, start, layout):
        self.start = start
        self.position = start # kvadrat v layout matriki
        self.room = layout # layout matrika v tistem trenutku

    def move(self, layout, layout_next):
        '''Checks the layout in the next second and if the robber can move he moves - else it's game over'''
        
        start = self.position
        x, y = start[0], start[1] # koordinati v matriki
        jump_to = 0
        possible_neighbors = []

        #if layout_next[x, y] != 0:
            
        neighbors = [(x, y+1), (x, y-1), (x+1, y), (x-1,y)]
        
        copy_neighbors = []
        #print(neighbors)
        for elt in neighbors:
            copy_neighbors.append(elt)
        for n in copy_neighbors: # preverimo če pademo ven iz matrike
            if n[0] < 0 or n[0] > len(layout[0])-1:
                if n in neighbors:    
                    neighbors.remove(n)
            if n[1] < 0 or n[1] > len(layout)-1:
                    
                if n in neighbors:
                    neighbors.remove(n)
        
        #print(neighbors)
        for n in neighbors:

            if layout_next[n[0], n[1]] == 0: #and layout[n[0], n[1]] == 0:
          #      print("h")
                possible_neighbors.append(n)
        
        if possible_neighbors != []:
            jump_to = np.array(random.choice(possible_neighbors))
            self.position = jump_to
            #print(jump_to)
        else:
            if layout_next[x, y] != 0:
            
                return "Game over"
        self.room = layout_next
        return jump_to



def finding_path(robber, room):
    """Finds the path. We assume the robber starts at a place that is not covered with a sensor.
    The number of steps is i, default value of i is 2 times the period of the room"""
    #robber_copy = copy.deepcopy(robber)
    #print(room.layout)
    got_path = False
    #room_copy = copy.deepcopy(room)
    #layout0 = room_copy.layout
    layout0 = room.layout
    #print(layout0)
    #print(layout00)
    #if not i:
     #   i = room_copy.period
    #print(robber.position)
    if layout0[robber.position[0], robber.position[1]] == 1:
        print("Robber's starting position is at an area covered with a sensor! Start elsewhere.")
    
    else:
        path = [list(robber.start)]

        layouts = [layout0]
        for j in range(room.period+1):
            layouts.append(room.room_at_time_n(1))
        #print(layouts)
        #print(room.period)
        for j in range(room.period+1):
            #print(robber.position)
            jump_to = robber.move(layouts[j], layouts[j+1])
            #print(robber.position)
            #jump_to = 0
            if jump_to == "Game over":
                #print(j)
                return None
            
            if list(robber.position) == list(robber.start) and len(path) >= room.period:
                if path.count(list(robber.start)) != len(path):
                    
                    path.append(list(robber.position))
                    print("Here is the path: " + str(path))
                    got_path = True
                    break
            else:
                path.append(list(robber.position))
            #robber.move(room.room_at_time_n(j), room_copy.room_at_time_n(j+1))
            #room_copy.room_at_time_n(1)
            
        #print(path)
        if got_path:
            #print("I didn't come back to the start but I did find some path.")
            return path
        else:
            
            return None

##s1 = Sensor(np.array([1, 1]), np.array([0, 1]), 2, 0)
##s2 = Sensor(np.array([1, 3]), np.array([1, 0]), 2, 0)
##s3 = Sensor(np.array([3, 3]), np.array([0, -1]), 2, 0)
##room1 = Room(np.array([4, 4]), [s1, s2, s3])
##
##layout0 = room1.layout
##layout1 = room1.room_at_time_n(1)
##layout2 = room1.room_at_time_n(1)
##layout3 = room1.room_at_time_n(1)
####layout4 = room1.room_at_time_n(1)
##
####print(layout0)
####print(layout1)
####print(layout2)
####print(layout3)
####print(layout4)
##
##s1 = Sensor(np.array([1, 1]), np.array([0, 1]), 2, 0)
##s2 = Sensor(np.array([1, 3]), np.array([1, 0]), 2, 0)
##s3 = Sensor(np.array([3, 3]), np.array([0, -1]), 2, 0)
##room1 = Room(np.array([4, 4]), [s1, s2, s3])
##
##start = np.array([3, 3]) # to mora bit nujno na ničli!
##robber = Robber(start, layout0)
##print(robber.position)
##robber.move(layout0, layout1)
##print(robber.position)
##robber.move(layout1, layout2)
##print(robber.position)
##robber.move(layout3, layout4)
##print(robber.position)
        
#from test_rooms import *
#room = room2
#print(room1.layout)
#finding_path(robber, room1)
























