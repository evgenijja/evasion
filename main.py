import threading

from room_operations import *
from test_rooms import *
from animation import *

if __name__ == "__main__":
    # choose a test room
    test_room = room0
    test_room = random_room()
    test_room = random_room(7, 9)

    animating = threading.Thread(target=run_animation, args=(test_room,))
    computing = threading.Thread(target=compute_homology, args=(test_room,))
    animating.start()
    computing.start()

    animating.join()
    computing.join()
