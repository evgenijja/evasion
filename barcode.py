from math import inf

lst = [(1, (2.0, inf)), (1, (8.0, inf)), (1, (14.0, inf)), (1, (20.0, inf)), (1, (26.0, inf)), (1, (32.0, inf)), (1, (38.0, inf)), (1, (44.0, inf)), (1, (50.0, inf)), (1, (56.0, inf)), (1, (12.0, inf)), (1, (24.0, inf)), (1, (36.0, inf)), (1, (48.0, inf)), (1, (58.0, inf)), (1, (0.0, inf)), (1, (3.0, inf)), (1, (9.0, inf)), (1, (15.0, inf)), (1, (22.0, inf)), (1, (28.0, inf)), (1, (33.0, inf)), (1, (39.0, inf)), (1, (45.0, inf)), (1, (52.0, inf)), (1, (59.0, inf)), (1, (3.0, inf)), (1, (7.0, inf)), (1, (11.0, inf)), (1, (15.0, inf)), (1, (19.0, inf)), (1, (23.0, inf)), (1, (27.0, inf)), (1, (31.0, inf)), (1, (35.0, inf)), (1, (39.0, inf)), (1, (43.0, inf)), (1, (47.0, inf)), (1, (51.0, inf)), (1, (55.0, inf)), (1, (59.0, inf)), (0, (0.0, inf))]
def filter_list(lst):
    new_list = []
    for elt in lst:
        x, y = 0,0
        if elt[1][1] == inf:
            y = 60 # perioda
            
        new_list.append([elt[1][0], y])
    return new_list

lst = filter_list(lst)

import matplotlib.pyplot as plt
import numpy as np

def draw_barcode(lst):
    height = 0
    for line in lst:
        
        x, y = line[0], line[1]
        if x < 60-1:
            height += 0.5
            plt.hlines(y= height, xmin = x, xmax = y, color='red')
        else:
            height += 0.5
            plt.hlines(y= height, xmin = x, xmax = y, color='blue')
        
    plt.show()

def persistance_diagram(lst):
    height = 0
    for line in lst:
        
        x, y = line[0], line[1]
        if x < 60-1:
            height += 0.5
            plt.vlines(x= height, ymin = x, ymax = y, color='red')
        else:
            height += 0.5
            plt.vlines(x= height, ymin = x, ymax = y, color='blue')
    X = [0, 60]
    Y = [0, 60]
    plt.plot(X, Y)
    plt.show()

lst.sort()
persistance_diagram(lst)
plt.show()
    
lst.sort(reverse=True)                

#plt.axhline(y= 1, xmin = 2, xmax = 5, color='red', linewidth = 5)
#plt.axhline(y= 2, xmin = 3, xmax = 6, color='red', linewidth = 5)
draw_barcode(lst)

plt.show()




