import numpy as np
import cv2
import urllib.request

async def image_manipulation(imageURL):
    image = await url_to_image(imageURL)

    title_ROI = await get_title_ROI(image)

    ### DEBUG
    show_image(title_ROI)

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

### DEBUG FUNCTION TO CHECK IM GETTING THE RIGHT IMAGE
def show_image(image):
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    return

async def get_title_ROI(image):
    height = image.shape[0]
    width = image.shape[1]

    return image[15:110, width-440:width-90]