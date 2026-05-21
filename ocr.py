# Handles image to text extraction using Tesseract
import re
from PIL import Image
import pytesseract

img = Image.open('samples/s2.png')
text = pytesseract.image_to_string(img)

# basic text cleaning
text  = text.lower()
text = re.sub(r'[^a-zA-Z0-9\s:/.-]', '', text)

#field extraction

# invoice date
date_pattern = r"\d{2}/\d{2}/\d{4}"

# gst num
gst_pattern = r"\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}"

# invoice number
invoice_keywords = [
    "invoice_number",
    "invoice_no",
    "invoice#",
    "bill no"
]