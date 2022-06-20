# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 08:34:01 2022

@author: Santiago
"""

import pytesseract
from PIL import Image
import pytesseract
from PIL import Image
import pytesseract
import imutils 
import pytesseract
import cv2
from numpy import random as np_random
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

path_image = 'C:/Users/Santiago/Documents/GitHub/gacetaces/captchas/img_captcha.png'



def incrementar_margenes(image_in):
    color = [0, 0, 0]
    image_out = cv2.copyMakeBorder(image_in, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value=color)
    return image_out


def resolver_captcha(path_image):
    img = cv2.imread(path_image, 0)
    img = incrementar_margenes(image_in=img)
    ret, gris = cv2.threshold(img, 75, 80, cv2.THRESH_BINARY_INV, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
    texto = pytesseract.image_to_string(gris, config="-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz --psm 3 --oem 0")
    return texto

b = pytesseract.image_to_string(Image.open(path_image))


c = pytesseract.image_to_string(path_image)


import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

im = Image.open(path_image) # the second one 
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
im.save('temp2.jpg')
text = pytesseract.image_to_string(Image.open('temp2.jpg'))
print(text)







import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread(path_image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Morph open to remove noise and invert image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening

# Perform text extraction
data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
print(data)

cv2.imshow('thresh', thresh)
cv2.imshow('opening', opening)
cv2.imshow('invert', invert)
cv2.waitKey()




import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open(path_image), lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

print(text)





import io
import requests
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance


img = Image.open(path_image)
img = img.convert('L')
img = img.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)
img = img.convert('1')
img.save('image.jpg')
imagetext = pytesseract.image_to_string(img)
print(imagetext)







import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

im = Image.open(img)  # img is the path of the image 
im = im.convert("RGBA")
newimdata = []
datas = im.getdata()

for item in datas:
    if item[0] < 112 or item[1] < 112 or item[2] < 112:
        newimdata.append(item)
    else:
        newimdata.append((255, 255, 255))
im.putdata(newimdata)

im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
im.save('temp2.jpg')
text = pytesseract.image_to_string(Image.open('temp2.jpg'),config='-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz', lang='eng')
print(text)








from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
path = path_image
img = Image.open(path)
img = img.convert('RGBA')
pix = img.load()
for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
            pix[x, y] = (0, 0, 0, 255)
        else:
            pix[x, y] = (255, 255, 255, 255)
text = pytesseract.image_to_string(Image.open(path_image))
print(text)





import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load image, grayscale, Otsu's threshold
image = cv2.imread(path_image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Blur and perform text extraction
thresh = cv2.GaussianBlur(thresh, (3,3), 0)
data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
print(data)

cv2.imshow('thresh', thresh)
cv2.waitKey()



subcadena = data[1:6]