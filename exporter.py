# Adds the Parsed data to CSV file

import csv

headers = ["DATE", 
            "TIME", 
            "FUEL TYPE", 
            "VOLUME", 
            "RATE",
            "AMOUNT", 
            "RECEIPT NO"]


data_insert_order = ["date",
                     "time",
                     "fuel_type",
                     "volume",
                     "rate",
                     "amount",
                     "receipt_no"]

def create_csv(file_path):
    with open(file_path,"w",newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

    return file_path

def add_data_to_csv(data,csv_file):
    export_data = [data[key] for key in data_insert_order]
    with open(csv_file, "a",newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(export_data)
    return csv_file





