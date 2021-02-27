import csv

class TermCacheBuilder():

    def __init__(self):
        pass

    def build_term_cache(self, terms_csv_path):

        with open(terms_csv_path, mode='r') as infile:
            reader = csv.reader(infile)
            next(reader, None)
            return {rows[0]:rows[1] for rows in reader}
