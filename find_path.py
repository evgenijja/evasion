# 1. find empty place in layout
# 2. for every second in the time period see if you can jump to one of the neighboring boxes undetected

class Robber:
    def __init__(self, start, layout):
        self.position = start # kvadrat v layout matriki
        self.room = layout # layout matrika v tistem trenutku

    def move(self, start, layout, layout_next):
        '''Checks the layout in the next second and if the robber can move he moves - else it's game over'''
        # predpostavim da se ne more gibat po diagonalah?
        x, y = start[0], start[1] # koordinati v matriki
        neighbors = [[x, y+1], [x, y-1], [x+1, y], [x-1,y]]
        
        for n in neighbors: # preverimo če pademo ven iz matrike
            if n[0] < 0 or n[0] > len(layout[0]):
                neighbors.remove(n)
            if n[1] < 0 or n[1] > len(layout):
                neighbors.remove(n)

        for n in neighbors:
            if layout_next[n[0], n[1]] == 0:
                self.start = n
            else:
                print("Game over")
                #raise Exception("Game over")
        self.room = layout_next

import numpy as np

from room import Sensor, Room   
        
# TEST

# NE DELA (ŠE) - mal so me indeksi zmedl

sensor1 = Sensor(np.array([1, 1]), np.array([1, 0]), 3, 0)
sensor2 = Sensor(np.array([1, 3]), np.array([1, 0]), 1, 1)
room = Room(np.array([4, 4]), [sensor1, sensor2])

layout1 = room.room_at_time_n(1)
layout2 = room.room_at_time_n(1)

start = np.array([0, 1])
robber = Robber(start, layout1)
robber.move(start, layout1, layout2)
