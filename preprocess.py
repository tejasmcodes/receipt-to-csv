import cv2
import numpy as np
from deskew import determine_skew

img = cv2.imread("samples/s5.png")

# None -> No Hard fixed sizes, scales the image by a factor of 2(x,y)
# interpolation is applied to get smoothen and sharp the edge of the enlarges text
# because small text causes OCR engine to fail
scaled = cv2.resize(img, None, fx=2.0, fy=2.0 , interpolation = cv2.INTER_CUBIC)

# convert to grayscale, because OCR engines struggles with RGB
grayscale = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)

#persepctive correction-deskewing
angle = determine_skew(grayscale)

(h, w) = grayscale.shape
center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
deskewed = cv2.warpAffine(grayscale, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# tight receipt cropping

cv2.imwrite(f"samples/OCR_ready/s5.png", deskewed)