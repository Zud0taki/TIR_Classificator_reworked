# import necessary libraries
import numpy as np


# define triplePixelCheck
# used to check if a label in the label_mat has at least 3 members
def triple_pixel_check(label, label_mat):
    label_counter = 1
    checked_label_list = []
    while label_counter <= label:
        if np.count_nonzero(label_mat == label_counter) >= 3:
            checked_label_list.append(label_counter)
            label_counter += 1
        else:
            label_counter += 1
    return checked_label_list
