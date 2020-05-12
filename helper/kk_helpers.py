from helper.image_helpers import *
from helper.filter_helpers import *
from helper.transformation_helpers import *
from helper.tesseract_helpers import *
from helper.word_helpers import *

import cv2
import numpy as np
import imutils
import math
import pytesseract
import time
import xlsxwriter as xcel

"Digunakan untuk mendeteksi area KK dan meluruskan gambar kk tersebut"
"Output dari fungsi ini adalah image"


def kk_area(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 10, 70, 70)
    ret, thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                              (np.ones((5, 5), np.uint8)))
    cnts = find_contour(thresh)

    return perspective_transform(image, cnts, (1600, 1200))


"Digunakan untuk mendeteksi area tabel"


def tabel_detector(image):
    image = imutils.resize(image, height=1000)

    grayImage = grayscale_conversion(image)
    thresh = otsu_thresholding(grayImage)
    thresh = cv2.bitwise_not(thresh)

    result = []
    ori_image = image
    image = imutils.resize(ori_image, height=1000)
    ratio_image = image_ratio(ori_image, image)

    grayImage = grayscale_conversion(image)
    thresh = otsu_thresholding(grayImage)
    thresh = cv2.bitwise_not(thresh)

    # MENDETEKSI AREA TABEL------------------------------------------------------------------------
    # Horizontal-----------------------------------------------------------------------------------
    horizontal = horizontal_filter(thresh, (10, 2), 2, 5)
    cnts = find_contour(horizontal)
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w < 400:
            cv2.drawContours(horizontal, [c], -1, (0, 0, 0), -1)

    # Vertical-------------------------------------------------------------------------------------
    vertical = vertical_filter(thresh, (2, 2), 2, 12)
    cnts = find_contour(vertical)
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if h < 120:
            cv2.drawContours(vertical, [c], -1, (0, 0, 0), -1)

    tabel_area = cv2.bitwise_or(vertical, horizontal)

    # show_image("HORIZONTAL", horizontal)
    # show_image("VERTICAL", vertical)
    # show_image("THROSH", thresh)
    # show_image("TABEL AREA", tabel_area)

    return tabel_area


"Digunakan untuk mendeteksi tabel dan meluruskannya"
"Output dari fungsi ini adalah array image"


def tabel_area(image):
    result = []
    ori_image = image
    image = imutils.resize(ori_image, height=1000)
    ratio_image = image_ratio(ori_image, image)

    grayImage = grayscale_conversion(image)
    thresh = otsu_thresholding(grayImage)
    thresh = cv2.bitwise_not(thresh)

    # MENDETEKSI AREA TABEL------------------------------------------------------------------------
    # Horizontal-----------------------------------------------------------------------------------
    horizontal = horizontal_filter(thresh, (10, 2), 2, 12)

    cnts = find_contour(horizontal)
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w < 400:
            cv2.drawContours(horizontal, [c], -1, (0, 0, 0), -1)
    # show_image("Horizontal", horizontal)

    # Vertical-------------------------------------------------------------------------------------
    vertical = vertical_filter(thresh, (2, 2), 2, 12)
    cnts = find_contour(vertical)
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if h < 120:
            cv2.drawContours(vertical, [c], -1, (0, 0, 0), -1)
    # show_image("Vertical", vertical)

    tabel_area = cv2.bitwise_or(vertical, horizontal)
    # show_image("TABEL AREA", tabel_area)

    cnts = find_contour(tabel_area)
    (cnts, boundingBoxes) = sort_contours(
        cnts, method="top-to-bottom")
    roi_index = 0
    for c in cnts:
        M = cv2.moments(c)
        c = c.astype("float")
        c *= ratio_image
        c = c.astype("int")
        x, y, w, h = cv2.boundingRect(c)

        if w > 500 and h > 200:
            roi = ori_image[y:y+h, x:x+w]
            roi = imutils.resize(roi, width=2000)

            gray_roi = grayscale_conversion(roi)
            thresh_roi = otsu_thresholding(gray_roi)
            thresh_roi = cv2.bitwise_not(thresh_roi)
            # show_image("T ROI", thresh_roi)

            # Horizontal Filter
            horTh2 = horizontal_filter(thresh_roi, (2, 2), 3, 20)
            horTh2 = hough_transform_noncanny(horTh2, 1000, iterariton=1)
            cntsth2 = find_contour(horTh2)
            for cnt in cntsth2:
                x, y, w, h = cv2.boundingRect(cnt)
                if w < 100:
                    cv2.drawContours(horTh2, [cnt], -1, (0, 0, 0), -1)
            # show_image("Horizontal", horTh2)

            # Vertical Filter
            verTh2 = vertical_filter(thresh_roi, (2, 2), 1, 20)
            # verTh2 = hough_transform_noncanny(verTh2, 1000, 1)

            cntsth2 = find_contour(verTh2)
            for cnt in cntsth2:
                x, y, w, h = cv2.boundingRect(cnt)
                if h < 200:
                    cv2.drawContours(verTh2, [cnt], -1, (0, 0, 0), -1)
            # show_image("Vertical", verTh2)

            tbl_border = cv2.bitwise_or(verTh2, horTh2)
            cntrs = find_contour(tbl_border)
            for cnt in cntrs:
                x, y, w, h = cv2.boundingRect(cnt)
                if h < 100:
                    cv2.drawContours(tbl_border, [cnt], -1, (0, 0, 0), -1)

            cntrs = find_contour(tbl_border)
            for cnt in cntrs:
                epsilon = 0.1*cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                hull = cv2.convexHull(cnt)
                cv2.drawContours(tbl_border, [hull], 0, (255, 255, 255), 2)

            # show_image("TABEL BORDER", tbl_border)

            out_tabel = cv2.bitwise_and(
                thresh_roi, 255 - tbl_border)
            out_tabel = cv2.morphologyEx(
                out_tabel, cv2.MORPH_OPEN, (2, 2), iterations=1)

            # MELURUSKAN TABEL---------------------------------------------------------------------
            # -------------------------------------------------------------------------------------
            contours = find_contour(tbl_border)
            max_area = 0
            coun = 0
            for incr in contours:
                area = cv2.contourArea(incr)
                if area > 1000:
                    if area > max_area:
                        max_area = area
                        best_cnt = incr
                        roi = cv2.drawContours(
                            roi, contours, coun, (0, 0, 0), 3)
                    coun += 1

            mask = np.zeros((gray_roi.shape), np.uint8)
            cv2.drawContours(mask, [best_cnt], 0, 255, -1)
            cv2.drawContours(mask, [best_cnt], 0, 0, 3)

            cntr_mask = find_contour(mask)

            out = np.zeros_like(gray_roi)
            out[mask == 255] = gray_roi[mask == 255]
            # show_image("OUT", out)

            finalsize = (1600, 320)
            final_out = perspective_transform(
                roi, cntr_mask, finalsize, 500, 200)

            # show_image("MASK", final_out)
            result.append(final_out)

    return result


"Digunakan untuk mengkonversi gambar menjadi text menggunakan Tesserac OCR"
"Output dari fungsi ini adalah array text"


def read_data_table(image):
    image = normalize_image(image)
    gamma = adjust_gamma(image, 1.2)
    blur = smoothen_image(gamma, 3)
    gray_image = grayscale_conversion(gamma)
    thresh = otsu_thresholding(gray_image)
    thresh = cv2.bitwise_not(thresh)

    # show_image("Image", gray_image)

    col_point, row_point = [], []

    # Menghilangkan Garis Tabel--------------------------------------------------------------------
    # Horizontal Filter
    horizontal = horizontal_filter(thresh, (2, 1), 3, 20)
    horizontal = hough_transform_noncanny(horizontal, 1000, iterariton=2)
    contours = find_contour(horizontal)
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 400:
            cv2.drawContours(horizontal, [cnt], -1, (0, 0, 0), -1)

    # Vertical Filter
    vertical = vertical_filter(thresh, (2, 1), 1, 20)
    vertical = hough_transform_noncanny(vertical, 1000, iterariton=2)
    contours = find_contour(vertical)
    (contours, boundingBoxes) = sort_contours(contours, method="left-to-right")
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h < 200:
            cv2.drawContours(vertical, [cnt], -1, (0, 0, 0), -1)
        else:
            if x > 15 and x < 1585:
                col_point.append((x, y, w, h))

    tbl_border = cv2.bitwise_or(horizontal, vertical)

    out_tabel = cv2.bitwise_and(thresh, 255 - tbl_border)
    # show_image("OUT TABEL", out_tabel)

    # out_tabel = cv2.bitwise_not(out_tabel)
    # ----------------------------------------------------------------------------------------------

    # Mendeteksi Koordinat Data---------------------------------------------------------------------
    horizontal = horizontal_filter(out_tabel, (10, 2), 2, 32)
    # show_image("HORIZONTAL s", horizontal)

    horizontal = hough_transform(horizontal, 100, 1000, 120)
    contours = find_contour(horizontal)
    (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if y < 74 or w < 300:
            cv2.drawContours(horizontal, [cnt], -1, (0, 0, 0), -1)
        else:
            if y < 305:
                row_point.append((x, y, w, h))

    # show_image("HORIZONTAL", horizontal)
    # ---------------------------------------------------------------------------------------------

    # Membaca Data KK per Cell---------------------------------------------------------------------
    all_data = []
    for i in range(0, len(row_point)):
        single_data = []
        for j in range(0, len(col_point)):
            startpoint = (col_point[j][0] + 3, row_point[i][1] - 5)

            if j == (len(col_point) - 1):
                endpoint = (1595, row_point[i][1] + 20)
            else:
                endpoint = (col_point[j+1][0] + 3, row_point[i][1] + 20)

            # Create Execution Indicator-----------------------------------------------------------
            cv2.rectangle(image, startpoint, endpoint, 0, 2)
            # -------------------------------------------------------------------------------------

            data_area = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
            data_area = out_tabel[startpoint[1]                                  :endpoint[1], startpoint[0]:endpoint[0]]
            data_area = cv2.bitwise_not(data_area)

            # Mengkonversi gambar menjadi text-----------------------------------------------------
            data, confidence = read_text_with_confidence(data_area)
            if data == "":
                data = "-"
            data = remove_all_enter(data)
            # data = img2text_whitelist(
            #     data_area, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-\s")
            # data = img2text_whitelist(data_area, "1234567890-")
            # -------------------------------------------------------------------------------------

            single_data.append([data, confidence])
        all_data.append(single_data)
    # ----------------------------------------------------------------------------------------------
    return all_data, image
