# Handles image to text extraction using Tesseract
import pytesseract

def extract_text(processed_img):
    text = pytesseract.image_to_string(processed_img)
    return text




