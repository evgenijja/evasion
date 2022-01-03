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

    def move(self) -> None:
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

    def __init__(self, dimension: npt.NDArray[int], sensors: list[Sensor]):
        self.dimension = dimension
        self.sensors = sensors
        self.compute_period()
        self.layout = self.create_layout()

    def compute_period(self) -> None:
        """Calculates the period; the time needed for all sensors to be back to the initial position.
        Period of d means that the layout of the sensors in the room at time t and t + d is equal."""
        steps = [2 * (sensor.steps_forward + sensor.steps_back) for sensor in self.sensors]
        lcm = np.lcm.reduce(steps)
        self.period = lcm if lcm else 1

    def time_passes(self) -> npt.NDArray[int]:
        """Simulates sensor movement in one time unit."""
        for sensor in self.sensors:
            sensor.move()
        self.layout = self.create_layout()
        return self.layout

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

    def layout_to_filtration(self, step: int, covered=False) -> list[list[float]]:
        """Transforms rooms layout to a filtration matrix.
        If covered is set to False, supervised cells get the infinity filtration,
        others get the filtration number equal to the argument step.
        If covered is True, free cells get the infinity filtration."""
        x, y = self.dimension
        filtration = np.zeros([x, y], dtype=float)
        for row in range(y):
            for cell in range(x):
                if self.layout[row][cell] == 0:
                    filtration_number = np.inf if covered else step
                    filtration[row][cell] += filtration_number
                else:
                    filtration_number = step if covered else np.inf
                    filtration[row][cell] += filtration_number
        return filtration.tolist()  # type: ignore

    def list_top_dimensial_cells(self, covered=False) -> list[list[list[float]]]:
        """Preprares s list of filtration matrices for the room at every time slice.
         If covered is set to False:
         At time t=0 we get the first matrix where all unsupervised cells have the filtration value 0.
         For all times between 0 and room period unsupervised cells have filtration value equal to t.
         If covered is set to True:
         At time t=0 we get the first matrix with supervised cells filtration number set to infinity.
         This list is useful for creating the (periodic) cubical complex."""
        top_dim_cells = []
        for i in range(self.period):
            top_dim_cells.append(self.layout_to_filtration(i, covered))
            self.time_passes()
        return top_dim_cells

    def create_complex(self, covered=False) -> gudhi.PeriodicCubicalComplex:
        """Creates and returns the gudhi.PeriodicCubicalComplex.
        If covered is set to True we get a cubical complex presenting the observed (covered) cells,
        else we get the complex out of unobserved cells."""
        return gudhi.PeriodicCubicalComplex(
            top_dimensional_cells=self.list_top_dimensial_cells(covered),
            periodic_dimensions=[True, False, False]
        )


    # TODO: determine which generators of H1(F, Z) represent paths a thief can take to avoid detection
