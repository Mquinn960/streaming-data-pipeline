from .irecord_writer import IRecordWriter

class DatabaseRecordWriter(IRecordWriter):

    db_client = None

    def __init__(self):
        pass

    def init_services(self):
        self.db_client = None

    def write_record(self, record):

        

        return True
