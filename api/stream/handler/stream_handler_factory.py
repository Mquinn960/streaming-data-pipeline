import typing

from .istream_handler import IStreamHandler
from .string_stream_handler import StringStreamHandler
from .stream_handler_enum import StreamHandlerEnum

class StreamHandlerFactory():

    def resolve_stream_handler(self, handler: StreamHandlerEnum) -> IStreamHandler:

        if handler == StreamHandlerEnum.string:
            return StringStreamHandler()
        else:
            return StringStreamHandler()
