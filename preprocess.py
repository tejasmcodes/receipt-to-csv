import cv2
import numpy as np
from deskew import determine_skew

img = cv2.imread("samples/s5.png")
original = img.copy()

# None -> No Hard fixed sizes, scales the image by a factor of 2(x,y)
# interpolation is applied to get smoothen and sharp the edge of the enlarges text
# because small text causes OCR engine to fail
scaled = cv2.resize(img, None, fx=2.0, fy=2.0 , interpolation = cv2.INTER_CUBIC)

# convert to grayscale, because OCR engines struggles with RGB
grayscale = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(grayscale,[5,5],0)

# use otsu's thresholding to create a binary mask->white and black
_, threshold = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# RETR_EXTERNAL only grabs the outermost booundary, ignoring the inner details
contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    largest_contour = max(contours, key = cv2.contourArea)

    # tight bounding box coordinates
    x,y,w,h = cv2.boundingRect(largest_contour)
    img_h, img_w = img.shape[:2]

    x_start= max(0,x)
    y_start= max(0,y)
    x_end = min(img_w, x+w)
    y_end = min(img_h,y+h)

    cropped_img = original[y_start:y_end, x_start:x_end]


# persepctive correction


# deskewing
angle = determine_skew(grayscale)

(h, w) = grayscale.shape
center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
deskewed = cv2.warpAffine(grayscale, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# tight receipt cropping

cv2.imwrite(f"samples/OCR_ready/s5.png", deskewed)