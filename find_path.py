# 1. find empty place in layout
# 2. for every second in the time period see if you can jump to one of the neighboring boxes undetected

import random


class Robber:
    def __init__(self, start, layout):
        self.start = start
        self.position = start # kvadrat v layout matriki
        self.room = layout # layout matrika v tistem trenutku


# tole je mal narodno spisano ampak dela? recimo?

# bom še mal olepšala, pobrisala printe itd
# IDEJA: move se premakne za 2 (!!) mesti v eno stran. Zakaj 2? V tem trenutku, ko sem
# tikala se mi je zdelo to smiselno, zdej mogoče ne več tok hah
# Ideja funkcije find path pa je, da pot išče randomly. Poišče kul sosede in se randomly premakne v enega.
# Torej proba se premaknit 10x (lahko povečamo) in mogoče mu uspe random najti pot.
# To funkcijo bi potem lahko večkrat pognale in mogoče v enem poskusu uspe najti, sicer obupa


    def move(self, layout, layout_next):
        '''Checks the layout in the next second and if the robber can move he moves - else it's game over'''
        # predpostavim da se ne more gibat po diagonalah?
        start = self.position
        x, y = start[0], start[1] # koordinati v matriki

        if layout_next[x, y] != 0:
            
            neighbors = [[(x, y+1), (x, y+2)], [(x, y-1), (x, y-2)], [(x+1, y), (x+2, y)], [(x-1,y), (x-2, y)]]
            #print(neighbors)
            copy_neighbors = []
            for elt in neighbors:
                copy_neighbors.append(elt)
            for pair in copy_neighbors: # preverimo če pademo ven iz matrike
                for n in pair:
                    #print((n, len(layout[0])))
                    if n[0] < 0 or n[0] > len(layout[0])-1:
                        if pair in neighbors: # šraufam
                     #       print("removam")
                            neighbors.remove(pair)
                        
                    if n[1] < 0 or n[1] > len(layout)-1:
                        #print((n, len(layout)))
                        if pair in neighbors:
                            #print("removam")
                            neighbors.remove(pair)
            #print("tle")
            #print(neighbors)
            possible_neighbors = []
            for pair in neighbors:
                #print(pair)
                for n in pair:
                 #   print(n)
                    if layout_next[n[0], n[1]] == 0:
                        possible_neighbors.append(n)
                    
                #else:
                 #   print("Game over")
                    #raise Exception("Game over")
            #path = []
            #print(possible_neighbors)
            if possible_neighbors != []:
                jump_to = np.array(random.choice(possible_neighbors))
                #print((list(jump_to), self.start))
                #if list(jump_to) == list(self.start): #and path != []:
                 #   print("We found a path!")
                #else:
                self.position = jump_to
                    #path.append(list(jump_to))
                #print(self.position)
            else:
                print("Game over")
            # random enega izbere, če ne gre pa pač na začetek
        self.room = layout_next


from room import *
import copy

def finding_path(robber : Robber, room : Room):

    # skačemo po 2 sekudni naprej (gledamo kao 2 koraka naprej, da se premane v bolj verjetno smer i guess)

    robber_copy = copy.deepcopy(robber)
    
    room_copy = copy.deepcopy(room)
    layout0 = room_copy.layout
    path = [list(robber_copy.start)]
    
    for i in range(2, 20, 2):
        robber_copy.move(layout0, room_copy.room_at_time_n(2))
        if list(robber_copy.position) == list(robber_copy.start) and path != [list(robber_copy.start)]:
            if path.count(list(robber_copy.start)) != len(path):
                #print((path, list(robber_copy.start)))
                #print(path.count(list(robber_copy.start)))
                path.append(list(robber_copy.position))
                print("Here is the path: " + str(path))
                break
        else:
            path.append(list(robber_copy.position))
            
    return path  




import numpy as np

from room import Sensor, Room   
        
# TEST

# NE DELA (ŠE) - mal so me indeksi zmedl

#sensor1 = Sensor(np.array([1, 1]), np.array([1, 0]), 3, 0)
#sensor2 = Sensor(np.array([1, 3]), np.array([1, 0]), 1, 1)
#room = Room(np.array([4, 4]), [sensor1, sensor2])

#layout1 = room.room_at_time_n(1)
#layout2 = room.room_at_time_n(1)

#start = np.array([0, 1])
#robber = Robber(start, layout1)
#robber.move(start, layout1, layout2)


# ENOSTAVEN PRIMER 2 X 2 MATRIKA TA PREVERIM SELF.MOVE
s1 = Sensor(np.array([1, 1]), np.array([0, 1]), 2, 0)
s2 = Sensor(np.array([1, 3]), np.array([1, 0]), 2, 0)
s3 = Sensor(np.array([3, 3]), np.array([0, -1]), 2, 0)
room = Room(np.array([4, 4]), [s1, s2, s3])

layout0 = room.layout
layout1 = room.room_at_time_n(1)
layout2 = room.room_at_time_n(1)
layout3 = room.room_at_time_n(1)
layout4 = room.room_at_time_n(1)

print(layout0)
print(layout1)
print(layout2)
print(layout3)
print(layout4)

start = np.array([3, 3]) # to mora bit nujno na ničli!
robber = Robber(start, layout0)
robber.move(layout0, layout2)

finding_path(robber, room)

from animation import *
#animation = Animation()
#animation.set_room(room)
#animation.run()


#start = np.array([
