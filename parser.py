# Sends raw OCR text to a vision API and returns the structured JSON
import re

def parse_receipt(text):
    # basic text cleaning
    text  = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s:/.-]', '', text)

    #clean ocr text
    replacement = {
            "1d":"id",
            "trk.": "trx.",
            "tuel": "fuel",
            "mobi le": "mobile",
            "vo tume": "volume",
            "mob.no": "mobile no",
            "receip": "receipt"
        }

    for wrong, correct in replacement.items():
        text = text.replace(wrong, correct)

    # date extraction
    def extract_date(text):
        date_pattern = r"\d{2}/\d{2}/\d{4}"
        lines = text.splitlines()
        for line in lines:
            match = re.search(date_pattern, line)
            if match:
                return match.group()
            
        return None

    date = extract_date(text)

    def extract_time(text):
        # some receipts contain only hours and minutes, so making seconds optional
        time_pattern = r"\d{2}:\d{2}(?::\d{2})?"
        lines = text.splitlines()
        for line in lines:
            match = re.search(time_pattern, line)
            if match:
                return match.group()
        return None
    
    time = extract_time(text)

    # fuel type extraction
    def extract_fuel_type(text):
        fuel_map = {
        "ms": "PETROL",
        "petrol": "PETROL",
        "xp95": "PETROL",
        "diesel": "DIESEL",
        "hsd": "DIESEL",
        "speed": "DIESEL"
        }

        lines = text.splitlines()
        for line in lines:
            for fuel in fuel_map:
                if fuel in line:
                    return fuel_map[fuel]

        return None
    
    fuel_type = extract_fuel_type(text)


    # fuel quantity/volume extraction
    def extract_fuel_volume(text):
        volume_keyword_types = [
            "volume",
            "quantity",
            "volume(L)",
            "qty",
            "volume(Ltr.)",
            "volume(Ltr. )",
            "litres",
            "liters"
        ]
        lines = text.splitlines()
        for line in lines:
            for keyword in volume_keyword_types:
                if keyword in line:
                    volume_line = line
                    volume_amount_pattern = r"\d+\.\d+"
                    match = re.search(volume_amount_pattern, volume_line)
                    return match.group()
        return None
    volume = extract_fuel_volume(text)
            


    # invoice number
    invoice_keywords = [
        "invoice_number",
        "invoice_no",
        "invoice#",
        "bill no",
        "Invoice no"
    ]
    
    return {
    "date": date,
    "time": time,
    "fuel_type": fuel_type,
    "volume": volume
    }