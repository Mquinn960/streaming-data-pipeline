import csv

class CsvReader():

    def __init__(self):
        pass

    def stream_csv_rows(self, csv_file):
        csv_input = csv.reader(csv_file)
        for row in csv_input:
            yield row
