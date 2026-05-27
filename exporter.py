# Adds the Parsed data to CSV file

import csv

def create_csv(file_path):
    headers = ["DATE", 
            "TIME", 
            "FUEL TYPE", 
            "VOLUME", 
            "RATE",
            "AMOUNT", 
            "RECEIPT NO"]

    with open(file_path,"w",newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

    return file_path

def add_data_to_csv(data,csv_file):
    new_row = data.values()
    with open(csv_file,"a",newline="", encoding="utf-8")as file:
        writer = csv.writer(file)
        writer.writerow(new_row)

    return csv_file





