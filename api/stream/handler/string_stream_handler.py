import io

from .istream_handler import IStreamHandler

class StringStreamHandler(IStreamHandler):

    def __init__(self):
        pass

    def handle(self, io_stream):

        return io.StringIO(io_stream.stream.read().decode("UTF8"), newline=None)
