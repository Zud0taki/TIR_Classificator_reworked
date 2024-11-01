# import necessary libraries
import cv2
import numpy as np
import requests
import time
import srtm

# https://github.com/tkrajina/srtm.py

# load srtm data
srtm_data = srtm.get_data()


# define homographyofpicture
# used to calculate the homography of the given picture
def homography_of_picture(img_src, pts_dst):
    srcshape = img_src.shape
    # Four corners of the src_img in pxl
    pts_src = np.array([[0, 0], [srcshape[1], 0], [srcshape[1], srcshape[0]], [0, srcshape[0]]])
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
    return h


# define lineSplitHomography
# used to split the txt-file and get the corner-real-world-coordinates
def line_split_homography(file_in, img):
    lines = []
    for line in file_in:
        lines.append(line)
    linesplit = lines[1].split('\t')
    x1 = linesplit[0]
    linesplit = linesplit[1].split('\n')
    y1 = linesplit[0]
    linesplit = lines[2].split('\t')
    x2 = linesplit[0]
    linesplit = linesplit[1].split('\n')
    y2 = linesplit[0]
    linesplit = lines[3].split('\t')
    x3 = linesplit[0]
    linesplit = linesplit[1].split('\n')
    y3 = linesplit[0]
    linesplit = lines[4].split('\t')
    x4 = linesplit[0]
    linesplit = linesplit[1].split('\n')
    y4 = linesplit[0]

    pts_dst = np.array(
        [[float(x1), float(y1)], [float(x2), float(y2)], [float(x3), float(y3)], [float(x4), float(y4)]])
    h = homography_of_picture(img, pts_dst)
    return h


# define homographypoints
# used to transform boundary points into real world coordinates
def homography_points(h, boundary_points):
    # multiplication of the matrices
    transformed_boundary_points = []
    for x in range(len(boundary_points)):
        xout = np.matmul(h, [boundary_points[x][1], boundary_points[x][0], 1])
        xout /= xout[2]
        # get height via SRTM
        lat = xout[0]
        long = xout[1]
        height = srtm_data.get_elevation(lat, long)
        transformed_boundary_points.append([lat, long, height])
    # test = response.text
    return transformed_boundary_points