# Entry point - connects ocr -> parser -> exporter
import os

from preprocess import preprocess_image
from ocr import extract_text
from parser import parse_receipt
from exporter import create_csv
from exporter import add_data_to_csv

img = preprocess_image("samples/s5.png")
text = extract_text(img)
parsed_data = parse_receipt(text)

csv_path = "outputs/receipt_data.csv"
if not os.path.exists(csv_path):
    create_csv(csv_path)

add_data_to_csv(parsed_data, csv_path)

with open(csv_path,"r", encoding="utf-8") as file:
    content  = file.read()
    print(content)


