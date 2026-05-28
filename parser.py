# Sends raw OCR text to a vision API and returns the structured JSON
import re
def extract_date(lines):
    # date_pattern = r"\d{2}[/-]\d{2}[/-]\d{4}"
    date_patterns = [

    # 2018/08/16
    r"\d{4}[/-]\d{1,2}[/-]\d{1,2}",

    # 05/07/2025
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",

    # 05-july-2025
    r"\d{1,2}[/-][a-zA-Z]{3,9}[/-]\d{2,4}",

    # july-05-2025
    r"[a-zA-Z]{3,9}[/-]\d{1,2}[/-]\d{2,4}"
]
    for line in lines:
        for date_pattern in date_patterns:
            match = re.search(date_pattern, line)
            if match:
                return match.group()
    return None


def normalize_date(date):
    if date is None:
        return None

    months= {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12"
    }

    separators_list = ["-","/","."," "]
    for separator in separators_list:
        if separator in date:
            date = date.split(separator)
            break
    
    for i in range(3):
        value = date[i]
        if value[0].isalpha():
            date[i] = months[value]
            month_index = i
            break
        else:
            month_index = 1

    dat = None
    year = None
    for i in range(3):
        if i == month_index:
            month = date[i]
            continue

        if len(date[i])==1:
            dat = f"0{date[i]}"
        elif len(date[i])==2:
            if dat is None:
                dat = date[i]
            else:
                year = date[i]
        else:
            year = date[i]

        
    normalize_date = f"{year}-{month}-{dat}"

    return normalize_date
        


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
    "xp100": "PETROL",
    "unleaded": "PETROL",

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

# rate extraction
def extract_rate(lines):
    rate_label_list = [
        "rate",
        "price",
        "rate/ltr",
        "rate/l",
        "unit price",
        "rsp",
        "price/ltr",
        "price/l",
        "per ltr",
        "per l",
    ]
    for line in lines:
        for rate_label in rate_label_list:
            if rate_label in line:
                rate_label_line = line
                rate_pattern = r"\d+(?:\.\d+)?"
                match = re.search(rate_pattern, rate_label_line)
                if match:
                    return match.group()


    return None


# amount extraction
def extract_amount(lines):
    amount_labels = [
        "amount",
        "total amount",
        "total",
        "sale",
        "total sale",
        "total amt",
        "net amount",
        "net amt",
        "paid amount",
        "amt paid"
    ]
    for line in lines:
        for label in amount_labels:
            if label in line:
                amount_label_line = line
                amount_pattern = r"\d+(?:\.\d+)?"
                match = re.search(amount_pattern, amount_label_line)
                if match:
                    return match.group()
                
    return None

def validate_amount(rate, volume, lines):
    calculated_amount = float(rate) * float(volume)
    calculated_amount = "{:.2f}".format(calculated_amount)
    extracted_amount = extract_amount(lines)
    if extracted_amount is None:
        return False
    extracted_amount = float(extracted_amount)
    return abs(calculated_amount - extracted_amount) < 1


# extract bill number -> critical for tracking transaction
def extract_receipt_no(lines):
    receipt_labels = [
        "bill no",
        "receipt no",
        "receipt id",
        "invoice no",
        "invoice number",
        "cash memo no",
        "memo no",
        "sale no"
    ]

    for line in lines:
        for label in receipt_labels:
            if label in line:
                parts = line.split(":")
                if len(parts)>1:
                    receipt_no_part = parts[1]
                    receipt_no_pattern = r"[a-zA-Z0-9/-]{3,}"
                    match = re.search(receipt_no_pattern,receipt_no_part)
                    if match:
                        return match.group()
                
    return None



   
        

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
            "l1tres": "litres",
            "ahount": "amount",
            "envoice": "invoice",
            "receiptt": "receipt"
        }

    for wrong, correct in replacement.items():
        text = text.replace(wrong, correct)

    return text


def parse_receipt(text):

    text = clean_text(text)

    lines = text.splitlines()
    
    date = extract_date(lines)
    normalized_date  = normalize_date(date)
    time = extract_time(lines)
    fuel_type = extract_fuel_type(lines)
    volume = extract_fuel_volume(lines)
    rate = extract_rate(lines)
    amount = extract_amount(lines)
    receipt_no = extract_receipt_no(lines)  

    return {
    "date": normalized_date,
    "time": time,
    "fuel_type": fuel_type,
    "volume": volume,
    "rate": rate,
    "amount": amount,
    "receipt_no": receipt_no
    }


if __name__ == "__main__":
    from preprocess import preprocess_image
    from ocr import extract_text
    preprocessed_image = preprocess_image("samples/s7.png")
    extracted_text = extract_text(preprocessed_image)
    parsed_data = parse_receipt(extracted_text)
    print(parsed_data)