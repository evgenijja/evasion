import numpy as np

from room import Sensor, Room

# simple sample room with a solution
sensor1 = Sensor(np.array([1, 1]), np.array([1, 0]), 2, 0)
sensor2 = Sensor(np.array([1, 3]), np.array([1, 0]), 1, 0)
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


