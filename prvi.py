import gudhi
import numpy as np



print(5)
a = gudhi.CubicalComplex([3, 3, 3], [1.0, 1.0, 1.0])
print(a)
print(a.betti_numbers())
print(6)

##from shared_code import check_pershombox_availability
##
##check_pershombox_availability
##from pershombox import cubical_complex_persistence_diagrams
##
##cubical_complex = np.array([[0, 2, 2],
##                            [1, 3, 2],
##                            [1, 1, 0]])
##
##dgms = cubical_complex_persistence_diagrams(cubical_complex)
##print(dgms)

