from room_operations import *
from test_rooms import *


if __name__ == "__main__":


    print("Initial room layout: ")
    print(room2.layout)

    print("Period: " + str(room2.period))

    print("Room after 2 time steps: ")
    print(time_step(room2, 2))

    print("About the complex:")
    about_complex(room2.create_complex())

    print("Possible one dimensional loops: " + str(one_dimensional_loop(room2)))
