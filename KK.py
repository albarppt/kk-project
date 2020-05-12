"""
    INERGI Family Card Analysis Project
    
    
    To run the program : >>> python3 KK.py
"""
from helper.image_helpers import *
from helper.kk_helpers import *


import cv2
import imutils
import xlsxwriter as xcel


"Core Function Merupakan fungsi utama system analisa kartu keluarga"


def core_function(image, image_index=1):
    image = adjust_gamma(image)

    # Detect KK Area-----------------------------------------------------------------
    kk = kk_area(image)
    # show_image("KK", kk)
    # -------------------------------------------------------------------------------

    # Detect Table-------------------------------------------------------------------
    tabels = tabel_area(kk)
    # -------------------------------------------------------------------------------

    # Read and Write Data Tabel------------------------------------------------------
    i = 0
    workbook = xcel.Workbook('output/Data KK #%s.xlsx' % image_index)
    for tbl in tabels:
        show_image("Tabel", tbl)

        # Read Data------------------------------------------------------------------
        datas, out_tabel = read_data_table(tbl)

        tabelname = ("output/KK #%s tabel %s.png" % (image_index, i+1))
        write_image(tabelname, out_tabel)
        show_image(tabelname, out_tabel)
        # ---------------------------------------------------------------------------

        # Save Data as Excel File----------------------------------------------------
        worksheet = workbook.add_worksheet('Tabel ' + str(i+1))

        # Declare the table name--------------------------------
        if i == 0:
            title = ["No.", "Nama Lengkap", "NIK", "Jenis Kelamin", "Tempat Lahir",
                     "Tanggal Lahir", "Agama", "Pendidikan", "Jenis Pekerjaan"]
        elif i == 1:
            title = ["No", "Status Perkawinan", "Status Hubungan Dalam Keluarga",
                     "Kewarganegaraan", "No.Paspor", "No.KITAP", "Ayah", "Ibu"]
        else:
            title = []

        cell_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': 'black', 'font_color': 'white'})
        for t_index in range(0, len(title)):
            worksheet.write(0, t_index, title[t_index], cell_format)

        row = 1
        cell_format = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter'})
        for data in datas:
            col = 1
            worksheet.write(row, 0, row, cell_format)
            for text, confidence in (data):
                worksheet.write(row, col, text + (" (Conf= %s)" %
                                                  confidence), cell_format)
                col += 1
            row += 1

        i += 1

    workbook.close()
    # -------------------------------------------------------------------------------


""" 
    Execution Mode digunakan untuk mengeksekusi Fungsi Utama dalam 2 mode.
        >>Mode 1 digunakan untuk mengeksekusi beberapa Image KK sekaligus
        >>Mode 2 Digunakan untuk mengeksekusi satu image KK saja

    "path" merupakan lokasi image kk yang akan dianalisa.
    Pada Mode 1 path dapat deitulis seperti berikut:

        "nama_folder/*g" 

    yang artinya system akan mengeksekusi 
    semua file yang namanya berakhiran "g" didalam folder tersebut.
"""


def execution_mode(mode=1, path="input/best_sample_data/*g"):
    if mode == 1:
        datas = load_all_images(path)
        imageindex = 1
        for data in datas:
            core_function(data)
            imageindex += 1

    elif mode == 2:
        image = load_original(path)
        core_function(image)

    else:
        print("You chose the wrong mode.")


# execution_mode(mode=1)
execution_mode(mode=2, path="input/best_sample_data/9_.jpg")
