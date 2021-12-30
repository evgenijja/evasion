import tkinter as tk
from room import *


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
        dim_x, dim_y = room.dimension
        self.sensor_reach = self.height / dim_y
        self.width = int(self.sensor_reach * dim_x)
        self.window.geometry("{0}x{1}".format(self.width, self.height))

    def animate(self):
        canvas = tk.Canvas(self.window, bg="white")
        canvas.pack(fill=tk.BOTH, expand=1)

        def my_mainloop():
            canvas.delete("all")
            for sensor in self.room.sensors:
                x, y = sensor.position
                canvas.create_rectangle(self.sensor_reach * x - self.sensor_reach,
                                        self.sensor_reach * y - self.sensor_reach,
                                        self.sensor_reach * x + self.sensor_reach,
                                        self.sensor_reach * y + self.sensor_reach, fill="purple")
            self.room.time_passes()
            self.window.update()
            self.window.after(self.speed, my_mainloop)

        self.window.after(0, my_mainloop)
        self.window.mainloop()

    def run(self) -> None:
        if self.room:
            self.animate()
        else:
            raise Exception("A room must be set in order to animate it. Please use .set_room(<your_room>) method.")


if __name__ == '__main__':
    sensor1 = Sensor(np.array([1, 1]), np.array([1, 0]), 2, 0)
    sensor2 = Sensor(np.array([1, 3]), np.array([1, 0]), 1, 0)
    sample_room = Room(np.array([4, 5]), [sensor1, sensor2])

    animation = Animation()
    animation.set_room(sample_room)
    animation.run()
