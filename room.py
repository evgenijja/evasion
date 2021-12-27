import copy
from typing import List
import numpy.typing as npt
import numpy as np


class Sensor:
    def __init__(self, start_position: npt.NDArray[int], direction: npt.NDArray[int], steps_forward: int,
                 steps_back: int):
        self.position = start_position
        self.direction = direction
        self.steps_forward = steps_forward
        self.steps_back = steps_back

    def move(self):
        """Moves the sensor for one step."""
        if self.steps_forward:
            self.position = self.position + self.direction
            self.steps_forward -= 1
            self.steps_back += 1
        else:
            self.direction = -self.direction
            self.position = self.position + self.direction
            self.steps_forward, self.steps_back = self.steps_back - 1, self.steps_forward + 1

    # TODO: Make a method that moves a sensor for the given number of steps.


class Room:
    period = None

    def __init__(self, dimension: npt.NDArray[int], sensors: List[Sensor]):
        self.dimension = dimension
        self.sensors = sensors
        self.compute_period()
        self.layout = self.create_layout()

    def compute_period(self) -> None:
        """Calculates the period; the time needed for all sensors to be back to the initial position.
        Period of d means that the layout of the sensors in the room at time t and t + d is equal."""
        steps = [2 * (sensor.steps_forward + sensor.steps_back) for sensor in self.sensors]
        self.period = np.lcm.reduce(steps)

    def time_passes(self) -> None:
        """Simulates sensor movement in one time unit."""
        for sensor in self.sensors:
            sensor.move()
        self.layout = self.create_layout()

    def time_slice(self, t: int) -> npt.NDArray[int]:
        """Returns a matrix representing the room at time t.
        The output matrix is of the same size as the room. Each field has a value of either 0 or 1.
        Number 0 represents a "free" field, that's a field that no sensor sees.
        Number 1 represents a supervised field. """
        time = t % self.period
        for _ in range(time):
            self.time_passes()
        return self.layout

    def create_layout(self) -> npt.NDArray[int]:
        """Creates a matrix that represents the initial layout. Ones in the matrix represent the supervised cells
        and zeros represent the "free" cells."""
        layout = np.zeros(self.dimension, dtype=int)
        dim_y, dim_x = self.dimension
        # TODO: improve those conditions (shorter code)
        for sensor in self.sensors:
            x, y = sensor.position
            if x == 0:
                # ce smo na robu, senzor vidi le 2 polji v x smeri
                if y == 0:
                    layout[-1][x] = 1
                elif y == dim_y:
                    layout[0][x] = 1
                else:
                    layout[-y][x] = 1
                    layout[-y + 1][x] = 1
            elif x == dim_x:
                if y == 0:
                    layout[-1][x - 1] = 1
                elif y == dim_y:
                    layout[0][x - 1] = 1
                else:
                    layout[-y][x - 1] = 1
                    layout[-y + 1][x - 1] = 1
            else:
                layout[-y][x - 1] = 1
                layout[-y][x] = 1
                layout[-y - 1][x - 1] = 1
                layout[-y - 1][x] = 1

        return layout


def time_step(room: Room, t: int) -> npt.NDArray[int]:
    """Calculates room layout after t time steps."""
    room_copy = copy.deepcopy(room)
    return room_copy.time_slice(t)


if __name__ == "__main__":
    print("simple test: 4 x 4 grid")
    sensor1 = Sensor(np.array([1, 1]), np.array([1, 0]), 2, 0)
    sensor2 = Sensor(np.array([1, 3]), np.array([1, 0]), 2, 0)
    sample_room = Room(np.array([4, 4]), [sensor1, sensor2])

    print("Initial room layout: ")
    print(sample_room.layout)

    print("Period: " + str(sample_room.period))

    print("Room after 2 time steps: ")
    print(time_step(sample_room, 2))
