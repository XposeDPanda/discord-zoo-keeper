import re
import numpy as np
import cv2
import urllib.request
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

async def get_title(imageURL):
    image = await url_to_image(imageURL)

    title_ROI = await get_title_ROI(image)

    title_ROI_RGB = cv2.cvtColor(title_ROI, cv2.COLOR_BGR2RGB)
    title_string = pytesseract.image_to_string(title_ROI_RGB)

    regex = re.compile('[^a-zA-z ]')
    title = regex.sub('', title_string)

    return title

async def url_to_image(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com)'
        }
    )
    resp = urllib.request.urlopen(req)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    return image

async def get_title_ROI(image):
    width = image.shape[1]

    title = image[50:80, width-440:width-90]

    ret, thresh = cv2.threshold(title,127,255,cv2.THRESH_BINARY_INV)
    return thresh