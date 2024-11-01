import time
import numpy as np
import random
from CheckNeighborhood import check_nbh
from CalculateHomography import line_split_homography, homography_points
from TriplePixelCheck import triple_pixel_check
from CheckLinearity import check_linearity
from ConcaveHull import *
from Export import export


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getNumberOfPolygons(acml_list):
    counter = 0
    # hop through the given list and count up everytime it hits a seperator
    for x in range(len(acml_list)):
        if acml_list[x][0][0] == 0:
            counter += 1
    return counter


def process_thresholding(read_img, coord_input, threshold, output_path):
    acml_list = []
    # hop through all images in img_input
    for f in range(len(read_img)):
        tac = time.time()
        img = read_img[f]
        # open textfile to the image in img_input
        with open(coord_input[f]) as coords_in:
            # calculate the homography of the picture with the coordinates from the txtfile
            h = line_split_homography(coords_in, img)
            # initiate the label_mat with an zeros/array from img_shape
            label_mat = np.zeros((img.shape), int)
            # initiate the label with a zero
            label = 0
            # get image dimensions
            dimY = img.shape[0]
            dimX = img.shape[1]
            # set threshold
            _threshold = float(threshold)
            for height in range(0, dimY - 1):
                y_row = img[height]
                if max(y_row) > _threshold:
                    for width in range(0, dimX - 1):
                        if img[height, width] > _threshold and label_mat[height, width] <1:
                            label = label + 1
                            label_mat = check_nbh(img, label_mat, label, _threshold, width, height)

            label_img = np.zeros((img.shape[0], img.shape[1], 3), float)
            labelclr = np.zeros([label_mat.max(), 3])

            # hop through the label matrix and color each labeled pixel group random
            # for i in range(label_mat.max() - 1):
            #     labelclr[i, :] = [random.random(), random.random(), random.random()]

            for x in range(img.shape[1]):
                for y in range(img.shape[0]):
                    if label_mat[y, x] > 0:
                        label_img[y, x, :] = labelclr[(label_mat[y, x] - 1), :]

            # initiate pts
            pts = []

            checked_label_list = triple_pixel_check(label, label_mat)

            counter = 0

            # initiate transformed boundary points
            transformed_boundary_points = []
            # fill the pts list with coordinates from the label matrix
            while counter <= (checked_label_list.__len__() - 1):
                for x in range(label_mat.shape[1]):
                    for y in range(label_mat.shape[0]):
                        if label_mat[y, x] == checked_label_list[counter]:
                            pts.append([y, x])

                # check in pts if the pixelgroups are linear
                nonlinear = check_linearity(pts)
                # proceed only if a pixelgroup has at least three members and is nonlinear
                # condition for the creation of polygons
                if pts.__len__() > 2 and nonlinear:
                    ch = ConcaveHull()
                    ch.loadpoints(pts)
                    ch.calculatehull()
                    # get the exterior points of a pixel group
                    boundary_points = np.vstack(ch.boundary.exterior.coords.xy).T
                    # use boundary points and the homography to get the transformed boundary points
                    # real world coordinates!
                    transformed_boundary_points = homography_points(h, boundary_points)
                    # save the transformed points in a list
                    for x in range(len(boundary_points)):
                        acml_list.append([boundary_points[x], transformed_boundary_points[x]])
                    # include a seperator for later use
                    acml_list.append([[0, 0], [0, 0, 0]])
                    pts.clear()
                    counter += 1
                    # cv2.waitKey()
                    # cv2.imshow('label_img', label_img_1)
                    # plt.show
                # if the condition in the beginning is not fullfilled - empty points for the next cycle
                else:
                    pts.clear()
                counter += 1
        tic = time.time()
        took = tic-tac
        print(f"{bcolors.WARNING}PROCESS | " + str(f + 1) + "/" + str((len(read_img))) + " in: ")
        nrpol = getNumberOfPolygons(acml_list)

    # get the data of the accumulated list, the treshold value, the temperature value and the outputpath
    # export the results

    # conv to temp
    # temp1 = temp

    outputpath = output_path
    export(acml_list, _threshold, outputpath) #temp1 --> add temperature - conv
