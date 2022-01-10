import copy
from typing import Tuple

from room import *


def time_step(room: Room, t: int) -> npt.NDArray[int]:
    """Calculates room layout after t time steps."""
    room_copy = copy.deepcopy(room)
    return room_copy.time_slice(t)


def whole_room_supervised(room: Room) -> bool:
    """Returns True if every cell of the room si seen by a sensor at least at some point.
    Returns False if this is not the case and there exist cells that are never seen."""
    room_copy = copy.deepcopy(room)
    layout = room_copy.layout
    for _ in room_copy.dimension:
        layout += room_copy.time_passes()
    return 0 not in layout


def about_complex(cubical_complex: gudhi.periodic_cubical_complex) -> None:
    """Prints some data about the cubical complex."""
    result_str = 'Periodic cubical complex is of dimension ' + repr(cubical_complex.dimension()) + ' - ' + \
                 repr(cubical_complex.num_simplices()) + ' simplices.'
    print(result_str)
    print("persistence:  " + repr(cubical_complex.persistence()))  # pairs(dimension, pair(birth, death))
    print("persistent_betti_numbers:  " + repr(cubical_complex.persistent_betti_numbers(np.inf, 1)))


def one_dimensional_loop(room: Room) -> list[Tuple[float, float]]:
    """"Function that calculates one dimensional loops in a cubical complex created based on room.
    If no such hole exists it returns [(-1, -1)]. Else, the output is a list of pairs (birth_time, death_time).
    NOTE: Also the diagonal movement is allowed!!"""
    cubical_complex = room.create_complex()
    period = room.period
    persistence = cubical_complex.persistence()
    loops = []
    if persistence:
        for dimension, pers in persistence:
            if dimension == 1:
                birth, death = pers
                if birth != death and birth >= period - 1:  # loops that are created before, are not around the torus
                    loops.append((dimension, pers))
    return loops if loops else [(-1, -1)]

# TODO: add functions for:
# -> creating random room with sensors
# -> answering:  Can you make sure that every point in the room is covered by at least one sensor at least part
#    of the time? How can homology help in detecting this?
# -> visualization (would be nice, not so important)
