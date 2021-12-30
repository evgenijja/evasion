import tkinter as tk


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

    def animate(self) -> None:
        """Main function that runs the animation. It creates the canvas, draws the sensors and updates room's layout."""
        canvas = tk.Canvas(self.window, bg="white")
        canvas.pack(fill=tk.BOTH, expand=1)

        def my_mainloop():
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
            self.room.time_passes()
            self.window.update()
            self.window.after(self.speed, my_mainloop)

        self.window.after(0, my_mainloop)
        self.window.mainloop()

    def run(self) -> None:
        """Checks if everything is prepared and starts the animation."""
        if self.room:
            self.animate()
        else:
            raise Exception("A room must be set in order to animate it. Please use .set_room(<your_room>) method.")


if __name__ == '__main__':
    from test_rooms import *

    animation = Animation()
    animation.set_room(room1)
    # animation.set_room(room2)
    animation.run()
