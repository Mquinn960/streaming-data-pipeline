import typing

from .iproducer import IProducer
from .basic_kafka_producer import BasicKafkaProducer
from .producer_enum import ProducerEnum

class ProducerFactory():

    def resolve_producer(self, producer: ProducerEnum) -> IProducer:

        if producer == ProducerEnum.kafka:
            return BasicKafkaProducer()
        else:
            return BasicKafkaProducer()
