import numpy as np
import random

from room import Sensor, Room

sensor1 = Sensor(np.array([2, 2]), np.array([0, 1]), 1, 0)
room0 = Room(np.array([10, 5]), [sensor1])

# simple sample room with a solution
sensor1 = Sensor(np.array([1, 1]), np.array([1, 0]), 2, 0)
sensor2 = Sensor(np.array([1, 3]), np.array([1, 0]), 2, 0)
room1 = Room(np.array([4, 4]), [sensor1, sensor2])

# example from the instructions
sensor1 = Sensor(np.array([1, 1]), np.array([0, 1]), 5, 0)
sensor2 = Sensor(np.array([6, 1]), np.array([1, 0]), 1, 4)
sensor3 = Sensor(np.array([5, 4]), np.array([0, 1]), 1, 1)
sensor4 = Sensor(np.array([3, 5]), np.array([0, 1]), 2, 0)
sensor5 = Sensor(np.array([7, 5]), np.array([0, 1]), 2, 2)
sensor6 = Sensor(np.array([4, 7]), np.array([-1, 0]), 3, 1)
room2 = Room(np.array([8, 8]), [sensor1, sensor2, sensor3, sensor4, sensor5, sensor6])

sensor1 = Sensor(np.array([1, 1]), np.array([1, 0]), 3, 0)
sensor2 = Sensor(np.array([1, 3]), np.array([1, 0]), 1, 1)
room3 = Room(np.array([4, 4]), [sensor1, sensor2])

# primer za katerga ni delou layout - če je bil senzor npr na zgornjem robu
sensor = Sensor(np.array([1, 0]), np.array([0, 1]), 2, 0)
room = Room(np.array([5, 5]), [sensor])


# GENERATING A RANDOM ROOM
def random_sensor(x_room: int, y_room: int) -> Sensor:
    # randomly choose a starting position
    start = np.array([random.randint(0, x_room), random.randint(0, y_room)])

    # chose one of the directions but make sure to check if the sensor starts on the boundary
    possible_directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    if start[0] == 0:
        possible_directions.remove([-1, 0])
    elif start[0] == x_room:
        possible_directions.remove([1, 0])
    if start[-1] == 0:
        possible_directions.remove([0, -1])
    elif start[-1] == y_room:
        possible_directions.remove([0, 1])

    direction = np.array(random.choice(possible_directions))

    # choose steps forward (steps back will be 0 at the start for all random sensors)
    # difference between starting position and border of the room in the direction the sensor is heading
    path = [direction[0] * start[0], direction[1] * start[1]]  # 1 komponenta direction bo ziher 0

    if path[0] == 0:  # sensor moves vertically
        if direction[1] < 0:  # check if it's going up or down
            forw = random.randint(0, start[1])
        else:
            forw = random.randint(0, y_room - start[1])

    elif path[1] == 0:  # sensor moves horizontally
        if direction[0] < 0:
            forw = random.randint(0, start[0])
        else:
            forw = random.randint(0, x_room - start[0])
    return Sensor(start, direction, forw, 0)


def random_room(y_room=10, x_room=10) -> Room:
    """Creates a room of dimension x_room x y_room with num_sensors randomly placed inside."""
    room_dim = np.array([y_room, x_room])
    n_sensors = random.randint(1, x_room + y_room)
    sensors = []
    for i in range(n_sensors):
        rand_sensor = random_sensor(x_room, y_room)
        sensors.append(rand_sensor)

    return Room(room_dim, sensors)


if __name__ == "__main__":
    r1 = random_room()
    from animation import *

    animation = Animation()
    animation.set_room(r1)
    animation.run()
