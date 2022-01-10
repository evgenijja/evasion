
import tkinter as tk
import time
from test_rooms import *
from find_path import Robber
import copy

class Animation:
    room = None
    width = 500
    height = 500
    sensor_reach = 0

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Evasion")
        self.speed = 600  # speed of the sensor movement in animation (in milliseconds)

    def set_room(self, room) -> None:
        """Sets the room and according to its dimensions sets the size of the canvas. Canvas height is fixed to 500,
        its width is relative to height according to the room size."""
        self.room = room
        self.layout = room.layout
        dim_y, dim_x = room.dimension
        self.sensor_reach = self.height / dim_y
        self.width = int(self.sensor_reach * dim_x)
        self.window.geometry("{0}x{1}".format(self.width, self.height))


    def animate_path(self, path) -> None:
        """Main function that runs the animation. It creates the canvas, draws the sensors and updates room's layout."""
        canvas = tk.Canvas(self.window, bg="white")
        canvas.pack(fill=tk.BOTH, expand=1)
        period = self.room.period

        
        i = 0
        step = 0
        self.room.time_passes()
        self.room.time_passes()
        # tole je šraufanje, glede na to kam sem štart postavla pri iskanju poti..
        # za ta specifičen primer pač mora bit tukej, bom probala nardit v splošnem za report
        
        def my_mainloop(i):
            canvas.delete("all")
            for sensor in self.room.sensors:
                x, y = sensor.position
                canvas.create_rectangle(self.sensor_reach * x - self.sensor_reach,
                                        self.sensor_reach * y - self.sensor_reach,
                                        self.sensor_reach * x + self.sensor_reach,
                                        self.sensor_reach * y + self.sensor_reach, fill="#e39229")
                canvas.create_oval(self.sensor_reach * x - 7,
                                   self.sensor_reach * y - 7,
                                   self.sensor_reach * x + 7,
                                   self.sensor_reach * y + 7, outline="#9e5c06", fill="#9e5c06")

            #uu, vv = self.robber_position
            #print(i)
            j = i % (2*len(path))
            #print(j)
            if j <= len(path)-1:
                uu, vv = path[j][0], path[j][1]
            
                u, v =  abs(vv-3), abs(uu-3)
            else:
                uu, vv = path[-(j-len(path))][0], path[-(j-len(path))][1]
            
                u, v = abs(vv-3), abs(uu-3)
            
            canvas.create_oval(self.sensor_reach * (u+0.5) - 20,
                                   self.sensor_reach * (v + 0.5) - 20,
                                   self.sensor_reach * (u+0.5) + 20,
                                   self.sensor_reach * (v+0.5) + 20, outline="#06489E", fill="#06489E")
            step = 0
            if (j == 0 or j == len(path)) and step != 0:
                i += 1
            step += 1
            time.sleep(0.5)
            #room_copy.time_passes()
            i += 1
            #self.robber.move(robber.room_layout, room_copy.layout)                   
            self.room.time_passes()
            self.window.update()
            self.window.after(self.speed, my_mainloop(i))

        self.window.after(0, my_mainloop(i))
        self.window.mainloop()

    def run_path(self, path) -> None:
        """Checks if everything is prepared and starts the animation."""
        if self.room:
            self.animate_path(path)
        else:
            raise Exception("A room must be set in order to animate it. Please use .set_room(<your_room>) method.")


def run_animation(room_to_animate):
    animation = Animation()
    animation.set_room(room_to_animate)
    animation.run()

from room import *

if __name__ == '__main__':
    animation = Animation()

    s1 = Sensor(np.array([1, 1]), np.array([0, 1]), 2, 0)
    s2 = Sensor(np.array([1, 3]), np.array([1, 0]), 2, 0)
    s3 = Sensor(np.array([3, 3]), np.array([0, -1]), 2, 0)
    room = Room(np.array([4, 4]), [s1, s2, s3])
    layout0 = room.layout

    # using sample room from the instructions
    animation.set_room(room)


    
    #animation.show_planar_slices()

    # uncomment to animate the room
    animation.run_path([[3, 3], [3, 2],[3, 1], [3, 2]])

    # uncomment to draw room's layout at time t = 3
    #animation.draw(3)
