from room_operations import *


if __name__ == "__main__":
    print("simple test: 4 x 4 grid")
    sensor1 = Sensor(np.array([1, 1]), np.array([1, 0]), 2, 0)
    sensor2 = Sensor(np.array([1, 3]), np.array([1, 0]), 0, 0)
    sample_room = Room(np.array([4, 4]), [sensor1, sensor2])

    print("Initial room layout: ")
    print(sample_room.layout)

    print("Period: " + str(sample_room.period))

    print("Room after 2 time steps: ")
    print(time_step(sample_room, 2))

    print("About the complex:")
    about_complex(sample_room.create_complex())

    print("Possible one dimensional loops: " + str(one_dimensional_loop(sample_room)))
