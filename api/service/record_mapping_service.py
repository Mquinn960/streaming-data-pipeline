class RecordMappingService():

    def __init__(self):
        pass

    def annotate_record(self, header, tuples):

        annotated_record = {}

        for i, item in enumerate(header):
            annotated_record[header[i]] = tuples[i]

        return annotated_record
