import cv2
import numpy as np


def horizontal_filter(thresh_image, kernel=(1, 1), dilate_iteration=1, horizontal_size_divider=30):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
    dilation = cv2.dilate(thresh_image, kernel, dilate_iteration)

    horizontal = np.copy(dilation)
    cols = horizontal.shape[1]
    horizontal_size = cols // horizontal_size_divider
    horizontalStructure = cv2.getStructuringElement(
        cv2.MORPH_RECT, (horizontal_size, 1))
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    return horizontal


def vertical_filter(thresh_image, kernel=(1, 1), dilate_iteration=1, vertical_size_divider=30):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
    dilation = cv2.dilate(thresh_image, kernel, dilate_iteration)

    vertical = np.copy(dilation)
    rows = vertical.shape[0]
    verticalsize = rows // vertical_size_divider
    verticalStructure = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, verticalsize))
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)

    return vertical


def find_contour(binary_image):
    cnts = cv2.findContours(binary_image, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    return cnts


def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)
