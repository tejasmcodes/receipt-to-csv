# Handles image to text extraction using Tesseract
import json
import re
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

pdf_path = "samples/teelabs.pdf"
pages = convert_from_path(pdf_path, dpi=300)

for index,page in enumerate(pages):
    image_name = f"page_{index+1}.png"
    page.save(f"samples/PDF_images/{image_name}","PNG")
    print(f"Saved: {image_name}")



img = Image.open("samples/PDF_images/page_1.png")
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
print(text)

# to mitigate the problem:
# perform ->binarization(thresholding), de-skewing, noise remvoval using opencv or pillow

