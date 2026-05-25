# Entry point - connects ocr -> parser -> exporter

from preprocess import preprocess_image
from ocr import extract_text
from parser import parse_receipt

img = preprocess_image("samples/s5.png")
text = extract_text(img)
parsed_data = parse_receipt(text)

print(parsed_data)

# {
#     "date": "", ->done
#     "time": "", -> done
#     "station_name": "",
#     "fuel_type": "", -> done
#     "quantity_liters": "", -> done
#     "price_per_liter": "",
#     "total_amount": "",
#     "payment_mode": "",
#     "transaction_id": ""
# } 