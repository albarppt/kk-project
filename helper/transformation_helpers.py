import cv2
import numpy as np
import imutils
from helper.filter_helpers import *
from helper.image_helpers import *


"""
    Digunakan untuk mendeteksi dan meluruskan kontur persegi
    Output dari fungsi ini adalah image
"""
def perspective_transform(image, contours, finaly_size_image, filter_w=500, filter_h=500):
    area_detected = False
    try:
        for c in contours:
            approx = cv2.approxPolyDP(c, 0.005 * cv2.arcLength(c, True), True)
            n, i = approx.ravel(), 0

            x, y, w, h = cv2.boundingRect(c)
            zero_x,  zero_y = x + int(w/2), y + int(h/2)

            if all([len(approx) == 4, w > filter_w, h > filter_h]):
                area_detected = True
                for j in n:
                    if(i % 2 == 0):
                        coordinat = (n[i], n[i + 1])

                    # QUADRANT DETECTOR--------------------------------------------
                    if i == 0:
                        cuad = 0
                        if coordinat[0] > zero_x and coordinat[1] < zero_y:
                            cuad = 1
                        if coordinat[0] < zero_x and coordinat[1] < zero_y:
                            cuad = 2
                        if coordinat[0] < zero_x and coordinat[1] > zero_y:
                            cuad = 3
                        if coordinat[0] > zero_x and coordinat[1] > zero_y:
                            cuad = 4
                    # -------------------------------------------------------------
                    i = i + 1

                if cuad == 1:
                    pts1 = np.float32(
                        [approx[1], approx[0], approx[2], approx[3]])
                if cuad == 2:
                    pts1 = np.float32(
                        [approx[0], approx[3], approx[1], approx[2]])
                if cuad == 3:
                    pts1 = np.float32(
                        [approx[3], approx[2], approx[0], approx[1]])
                if cuad == 4:
                    pts1 = np.float32(
                        [approx[2], approx[1], approx[3], approx[0]])

                pts2 = np.float32(
                    [[0, 0], [finaly_size_image[0], 0], [0, finaly_size_image[1]], finaly_size_image])
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                result = cv2.warpPerspective(image, matrix, finaly_size_image)

        if area_detected == False:
            print("----------------------------------------")
            print("The area you want is not detected")
            print("----------------------------------------")
            result = 0      
    except Exception:
        print("----------------------------------------")
        print("Failed to find contours")
        print("----------------------------------------")
        result = 0

    return result


"""
    Hough Transform
"""
def hough_transform_noncanny(mask, maxLG=200, thres=200, iterariton=1):
    for it in range(0, iterariton):
        lines = cv2.HoughLinesP(mask, 1, np.pi / 180, thres, minLineLength=100, maxLineGap=maxLG)
        if lines is not None:
            for i in range(0, len(lines)):
                l = lines[i][0]
                cv2.line(mask, (l[0], l[1]), (l[2], l[3]),
                        (255, 255, 255), 2, cv2.LINE_AA)
    return mask

def hough_transform(mask, minLL=100, maxLG=200, thres=100):
    gray = grayscale_conversion(mask)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi/180, threshold=thres,
                            lines=np.array([]), minLineLength=minLL, maxLineGap=maxLG)
    a, b, c = lines.shape
    for i in range(a):
        cv2.line(gray, (lines[i][0][0], lines[i][0][1]), (lines[i]
                                                        [0][2], lines[i][0][3]), (255, 255, 255), 3, cv2.LINE_AA)

    return gray
