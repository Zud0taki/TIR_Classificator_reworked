# define checknbh - checking the neighborhood of labeled pixels
def check_nbh(img, label_mat, label, threshold, x, y):
    temp_coords = [x, y]
    label_mat[y, x] = label
    # as long as the temp_coords list is not zero = active -> check coordinates -> index and label them -> delete list with indices
    while not len(temp_coords) == 0:
        indexX = len(temp_coords) - 2
        indexY = len(temp_coords) - 1
        checkX = temp_coords[indexX]
        checkY = temp_coords[indexY]
        del temp_coords[indexX:]
        label_mat[y, x] = label
        # check in the neighborhood of 3x3 pixels
        for i in range(3):
            for j in range(3):
                currX = checkX - 1 + i
                currY = checkY - 1 + j
                # check if pixel is possible (border-check)
                if currX < 0 or currX > (img.shape[1] - 1) or currY < 0 or currY > (img.shape[0] - 1):
                    isborder = True
                else:
                    isborder = False
                # check if pixel is not out of bounds and pixel exceeds threshold and pixel is not already labeled
                if not isborder and img[currY, currX] > threshold and label_mat[currY, currX] < 1:
                    checkTresh = img[currY, currX]
                    checkLabel = label_mat[currY, currX]
                    label_mat[currY, currX] = label
                    temp_coords.append(currX)
                    temp_coords.append(currY)
        # return the label matrix
    return label_mat
