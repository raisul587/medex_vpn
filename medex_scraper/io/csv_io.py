import csv
import os
from ..config import CSV_FILE, COLUMNS


def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(COLUMNS)


def write_to_csv(data_list):
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in data_list:
            if len(row) != len(COLUMNS):
                row = row + [None] * (len(COLUMNS) - len(row))
            writer.writerow(row)
