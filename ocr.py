# Handles image to text extraction using Tesseract
import pytesseract

def extract_text(processed_img):
    text = pytesseract.image_to_string(processed_img)
    return text

if __name__ == "__main__":
    from preprocess import preprocess_image
    preprocessed_image = preprocess_image("samples/s7.png")
    extracted_text = extract_text(preprocessed_image)
    print(extracted_text)



