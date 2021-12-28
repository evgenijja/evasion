import copy
from typing import Tuple

from room import *


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

# TODO: add functions for:
# -> creating random room with sensors
# -> answering:  Can you make sure that every point in the room is covered by at least one sensor at least part
#    of the time? How can homology help in detecting this?
# -> visualization (would be nice, not so important)
