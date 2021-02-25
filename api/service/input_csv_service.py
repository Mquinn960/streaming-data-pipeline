from stream.handler.stream_handler_enum import StreamHandlerEnum
from stream.handler.stream_handler_factory import StreamHandlerFactory
from stream.producer.producer_enum import ProducerEnum
from stream.producer.producer_factory import ProducerFactory
from file_io.csv_reader import CsvReader 
from .record_mapping_service import RecordMappingService

class InputCsvService():

    handler_factory = None
    handler = None

    producer_factory = None
    producer = None

    mapping_service = None

    reader = None

    def __init__(self):
        self.init_services()

    def init_services(self):
        self.handler_factory = StreamHandlerFactory()
        self.handler = self.handler_factory.resolve_stream_handler(StreamHandlerEnum.string)

        self.producer_factory = ProducerFactory()
        self.producer = self.producer_factory.resolve_producer(ProducerEnum.kafka)

        self.mapping_service = RecordMappingService()

        self.reader = CsvReader()

    def parse_input_csv(self, input_file, includes_header=True):

        # Handle the expected input stream
        input_stream = self.handler.handle(input_file)

        # Stream CSV rows
        row_generator = self.reader.stream_csv_rows(input_stream)

        row_count = 0
        header_row = None

        # Feed to required producer
        for row in row_generator:
            if includes_header:
                if row_count == 0:
                    header_row = row
                else:
                    mapped_record = self.mapping_service.annotate_record(header_row, row)
                    self.producer.produce(mapped_record)
            else:
                self.producer.produce(row)

            row_count += 1

        return True
