import sys
import getopt
import glob
import cv2 as cv
# from Threshold import process_thresholding
from Threshold import process_thresholding
import time


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


def collect_args(argv):
    inputpath: str = ''
    outputpath: str = ''
    threshold: str = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:t:", ["ifile=", "ofile=", "thresh="])
    except getopt.GetoptError:
        print("StartCollection.py -i <inputpath> -o <outputpath> -t <threshold>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("StartCollection.py -i <inputpath> -o <outputpath> -t <threshold>")
            sys.exit()
        elif opt in ("-i", "-ifile"):
            inputpath = arg
        elif opt in ("-o", "ofile"):
            outputpath = arg
        elif opt in ("-t", "-thresh"):
            threshold = arg
    print(f"{bcolors.OKBLUE}INFO | path to input is:{bcolors.ENDC}")
    print(inputpath)
    print(f"{bcolors.OKBLUE}INFO | path to output is:{bcolors.ENDC}")
    print(outputpath)
    print(f"{bcolors.OKBLUE}INFO | given threshold is:{bcolors.ENDC}")
    print(threshold)
    return inputpath, outputpath, threshold


def read_inputs(input_path):
    img_input = glob.glob(input_path + "/*.tif")
    coord_input = glob.glob(input_path + "/*txt")
    if len(img_input) == len(coord_input):
        print(f"{bcolors.OKBLUE}INFO | input reading status:{bcolors.ENDC}")
        print("SUCCESS")
        return img_input, coord_input
    else:
        print(f"{bcolors.FAIL}ERROR | input reading status:{bcolors.ENDC}")
        print("uneven input lengths between images and coord-files")


def read_images(img_input):
    read_img = []
    for img in img_input:
        im = cv.imread(img, -1)
        read_img.append(im)
    print(f"{bcolors.OKBLUE}INFO | reading images to list of arrays:{bcolors.ENDC}")
    print("SUCCESS")
    return read_img


if __name__ == "__main__":
    tac = time.time()
    inputpath, outputpath, threshold = collect_args(sys.argv[1:])
    img_input, coord_input = read_inputs(inputpath)
    read_img = read_images(img_input)
    print(f"{bcolors.OKBLUE}INFO | start processing the following number of images:{bcolors.ENDC}")
    print(str(len(read_img)))
    process_thresholding(read_img, coord_input, threshold, outputpath)
    tic = time.time()
    print(tic - tac)
