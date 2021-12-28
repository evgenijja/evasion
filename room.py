import copy
from typing import List, Tuple

import gudhi
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

    def layout_to_filtration(self, step: int) -> List[List[float]]:
        """Transforms rooms layout to a filtration matrix. Supervised cells get the infinity filtration,
        others get the filtration number equal to the argument step."""
        x, y = self.dimension
        filtration = np.zeros([x, y], dtype=float)
        for row in range(y):
            for cell in range(x):
                if self.layout[row][cell] == 0:
                    filtration[row][cell] += step
                else:
                    filtration[row][cell] = np.inf
        return filtration.tolist()

    def list_top_dimensial_cells(self) -> List[List[List[float]]]:
        """Preprares s list of filtration matrices for the room at every time slice.
         At time t=0 we get the first matrix where all unsupervised cells have the filtration value 0.
         For all times between 0 and room period unsupervised cells have filtration value equal to t.
         This list is useful for creating the (periodic) cubical complex."""
        top_dim_cells = []
        for i in range(self.period):
            top_dim_cells.append(self.layout_to_filtration(i))
            self.time_passes()
        return top_dim_cells

    def create_complex(self) -> gudhi.PeriodicCubicalComplex:
        """Creates and returns the gudhi.PeriodicCubicalComplex."""
        return gudhi.PeriodicCubicalComplex(
            top_dimensional_cells=self.list_top_dimensial_cells(),
            periodic_dimensions=[True, False, False]
        )


def time_step(room: Room, t: int) -> npt.NDArray[int]:
    """Calculates room layout after t time steps."""
    room_copy = copy.deepcopy(room)
    return room_copy.time_slice(t)


def about_complex(cubical_complex: gudhi.periodic_cubical_complex) -> None:
    """Prints some data about the cubical complex."""
    result_str = 'Periodic cubical complex is of dimension ' + repr(cubical_complex.dimension()) + ' - ' + \
                 repr(cubical_complex.num_simplices()) + ' simplices.'
    print(result_str)
    print("persistence:  " + repr(cubical_complex.persistence()))  # pairs(dimension, pair(birth, death))
    print("compute_persistence:  " + repr(cubical_complex.compute_persistence()))
    print("cofaces_of_persistence_pairs:  " + repr(cubical_complex.cofaces_of_persistence_pairs()))
    print("persistent_betti_numbers:  " + repr(cubical_complex.persistent_betti_numbers(np.inf, 1)))


def one_dimensional_loop(room: Room) -> List[Tuple[float, float]]:
    """"Function that calculates one dimensional loops in a cubical complex created based on room.
    If no such hole exists it returnes [(-1, -1)]. Else, the output is a list of pairs (birth_time, death_time).
    NOTE: Also the diagonal movement is allowed!!"""
    cubical_complex = room.create_complex()
    persistence = cubical_complex.persistence()
    loops = []
    if persistence:
        for dimension, pers in persistence:
            if dimension == 1:
                birth, death = pers
                if birth != death:
                    loops.append((dimension, pers))
    return loops if loops else [(-1, -1)]


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

    print("About the complex:")
    about_complex(sample_room.create_complex())

    print("Possible one dimensional loops: " + str(one_dimensional_loop(sample_room)))
