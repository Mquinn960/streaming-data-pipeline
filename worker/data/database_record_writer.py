import psycopg2

from .irecord_writer import IRecordWriter

class DatabaseRecordWriter(IRecordWriter):

    db_client = None

    db = "menustats"
    user = "menustatsuser"
    password = "examplepw"
    host = "localhost"
    port = "5432"

    def __init__(self):
        self.init_services()

    def __del__(self):
        self.db_client.close()

    def init_services(self):
        self.db_client = psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)

    def write_record(self, record):

        cursor = self.db_client.cursor()

        for term in record['term_matches']:

            # Insert each base term
            self.insert_term(cursor, term[0], term[1])

            # Insert match records
            self.insert_match(cursor, record['MenuId'], term[0], record['ProductName'], record['ProductDescription'])
        
        print("Records inserted successfully")

        return True

    def insert_term(self, cursor, term_id, term_name):

        term_insert = "INSERT INTO term(term_id, term_name) VALUES('{}', '{}') ON CONFLICT DO NOTHING;"
        term_insert_query = term_insert.format(term_id, term_name)

        try:
            cursor.execute(term_insert_query)
        except:
            self.db_client.rollback()
            print("Term insertion failed")
        else:
            self.db_client.commit()

    def insert_match(self, cursor, menu_id, term_id, prod_name, prod_desc):

        match_insert = "INSERT INTO match(menu_id, term_id, product_name, product_description) VALUES('{}', '{}', '{}', '{}') ON CONFLICT DO NOTHING;"
        match_insert_query = match_insert.format(menu_id, term_id, prod_name, prod_desc)

        try:
            cursor.execute(match_insert_query)
        except:
            self.db_client.rollback()
            print("Match insertion failed")
        else:
            self.db_client.commit()
