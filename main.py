from room_operations import *
from test_rooms import *


if __name__ == "__main__":

    # choose a test room
    test_room = room2

    print("Initial room layout: ")
    print(test_room.layout)

    print("Room after 2 time steps: ")
    print(time_step(test_room, 2))

    print("Sensors are scanning the whole room."
          if whole_room_supervised(test_room)
          else "Room has blind spots where the intruder can not be seen.")

    print("Period: " + str(test_room.period))

    print("About the complex:")
    about_complex(test_room.create_complex())

    print("Possible one dimensional loops: " + str(one_dimensional_loop(test_room)))
