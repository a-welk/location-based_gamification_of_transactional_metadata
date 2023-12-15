import csv

filename = "/path/to/transactions.csv"
rows_to_read = 2

with open(filename, "r") as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i >= rows_to_read:
            break
        print(row)
