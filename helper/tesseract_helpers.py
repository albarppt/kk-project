import cv2 as cv
import pytesseract
# import utils.image_helpers as image_helpers

from PIL import Image
from tesserocr import PyTessBaseAPI, PSM, RIL, OEM

""" Get bounding boxes of parts of image identified as text

Returns:
	array -- List of coordinates
"""


def get_text_bounding_boxes(image, psm=12):
    bounding_boxes = []

    height, width = image.shape[:2]

    if height <= 0 or width <= 0:
        return bounding_boxes

    image_pil = Image.fromarray(image)  # Load PIL image from numpy

    api = PyTessBaseAPI(psm=psm, oem=OEM.LSTM_ONLY)

    try:
        # api.SetVariable('textord_tabfind_find_tables', 'true')
        # api.SetVariable('textord_tablefind_recognize_tables', 'true')
        api.SetImage(image_pil)

        api.Recognize()

        boxes = api.GetComponentImages(RIL.TEXTLINE, True)

        for (im, box, _, _) in boxes:
            x, y, w, h = box['x'], box['y'], box['w'], box['h']

            bounding_boxes.append((x, y, w, h))
    finally:
        api.End()

    return bounding_boxes


""" Reads text and outputs the text as well as confidence

Returns:
	string 	-- The text obtained from Tesseract
	integer	--	The confidence
"""


def read_text_with_confidence(image, lang='fast_ind', path='/usr/share/tesseract-ocr/5/tessdata', psm=4, whitelist=''):
    height, width = image.shape[:2]

    if height <= 0 or width <= 0:
        return '', 0

    image_pil = Image.fromarray(image)

    api = PyTessBaseAPI(lang=lang, psm=psm, path=path, oem=OEM.LSTM_ONLY)

    try:
        api.SetImage(image_pil)

        if whitelist != '':
            api.SetVariable('tessedit_char_whitelist', whitelist)

        api.Recognize()

        text = api.GetUTF8Text()
        confidence = api.MeanTextConf()
    except Exception:
        print("[ERROR] Tesseract exception")
    finally:
        api.End()

    return text, confidence


""" Read a single line text found in an image
	Uses psm mode = 6 and oem = 1 (LSTM)

Returns:
	string -- The output text produced by Tesseract
"""


def read_one_line(image, lang="ind_fast", preserve_space=True, digits=False, only_alpha=False, date=True):
    config = "--psm 6 --oem 1"

    height, width = image.shape[:2]

    if height <= 0 or width <= 0:
        return ''

    if preserve_space == True:
        config = config + " -c preserve_interword_spaces=1"

    return pytesseract.image_to_string(image, lang=lang, config=config)


""" Read all text found in an image
	Uses psm mode = 4 and oem = 1 (LSTM)

Returns:
	string -- The output text produced by Tesseract
"""


def read_all_text(image, lang="ind_fast", preserve_space=True, psm=4):
    config = "--psm " + str(psm) + " --oem 1"

    height, width = image.shape[:2]

    if height <= 0 or width <= 0:
        return ''

    if preserve_space == True:
        config = config + "  -c preserve_interword_spaces=1"

    return pytesseract.image_to_string(image, lang=lang, config=config)


def img2text_whitelist(image, whitelist='123'):
    custom_config = r'-c tessedit_char_whitelist='+whitelist+' --psm 6'
    return pytesseract.image_to_string(image, config=custom_config)
