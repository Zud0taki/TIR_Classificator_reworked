# import numpy to calculate with arrays
import numpy as np


# definition of checkLinearity using the points (pts) from the thresholding
def check_linearity(pts):
    # get point coordinates
    coordinate_1 = np.array(pts[0])
    coordinate_2 = np.array(pts[1])
    # calculate the direction vector
    direction_vector = coordinate_2 - coordinate_1
    # initialize the nonlinear bool as true
    nonlinear = True
    # hop through the points and check if the direction vector changes - set nonlinear true or false
    for x in range(1, len(pts) - 1):
        coordinate_1 = np.array(pts[x])
        coordinate_2 = np.array(pts[x + 1])
        compare_vector = coordinate_2 - coordinate_1
        if compare_vector[0] == direction_vector[0] and compare_vector[1] == direction_vector[1]:
            nonlinear = False
        else:
            nonlinear = True
            break
    return nonlinear
