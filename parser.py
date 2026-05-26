# Sends raw OCR text to a vision API and returns the structured JSON
import re
def extract_date(lines):
    date_pattern = r"\d{2}[/-]\d{2}[/-]\d{4}"
    for line in lines:
        match = re.search(date_pattern, line)
        if match:
            return match.group()
    return None

def extract_time(lines):
    # some receipts contain only hours and minutes, so making seconds optional
    time_pattern = r"\d{2}:\d{2}(?::\d{2})?"
    for line in lines:
        match = re.search(time_pattern, line)
        if match:
            return match.group()
    return None

# fuel type extraction
def extract_fuel_type(lines):
    fuel_map = {
        "ms": "PETROL",
        "petrol": "PETROL",
        "xp95": "PETROL",
        "diesel": "DIESEL",
        "hsd": "DIESEL",
        "speed": "DIESEL"
        }
    for line in lines:
        for fuel, normalized in fuel_map.items():
            if fuel in line:
                return normalized

    return None

# fuel quantity/volume extraction
def extract_fuel_volume(lines):
    volume_keyword_types = [
        "volume",
        "quantity",
        "volume(l)",
        "qty",
        "volume(ltr.)",
        "volume(ltr. )",
        "litres",
        "liters"
        ]
    for line in lines:
        for keyword in volume_keyword_types:
            if keyword in line:
                volume_line = line
                volume_amount_pattern = r"\d+(?:\.\d+)?"
                match = re.search(volume_amount_pattern, volume_line)
                if match:
                    return match.group()
    return None

# invoice number
    invoice_keywords = [
        "invoice_number",
        "invoice_no",
        "invoice#",
        "bill no",
        "Invoice no"
    ]

def clean_text(text):
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
            "receip": "receipt",
            "vo1ume": "volume",
            "l1ters": "liters",
            "l1tres": "litres"
        }

    for wrong, correct in replacement.items():
        text = text.replace(wrong, correct)

    return text


def parse_receipt(text):

    text = clean_text(text)
    
    lines = text.splitlines()
    
    date = extract_date(lines)
    time = extract_time(lines)
    fuel_type = extract_fuel_type(lines)
    volume = extract_fuel_volume(lines)
            

    return {
    "date": date,
    "time": time,
    "fuel_type": fuel_type,
    "volume": volume
    }