import json

from kafka import KafkaProducer
from kafka import KafkaClient

from .iproducer import IProducer

class BasicKafkaProducer(IProducer):

    producer = None
    kafka_instance = ['kafka:9091']

    active_topic = 'input-csv'

    def __init__(self):
        self.init_services()

    def init_services(self):

        self.producer = KafkaProducer(bootstrap_servers = self.kafka_instance, value_serializer=lambda m: json.dumps(m).encode('ascii'))

    def alter_topics(self):

        client = KafkaClient(bootstrap_servers = self.kafka_instance)

        future = client.cluster.request_update()
        client.poll(future=future)

        metadata = client.cluster

        if self.active_topic not in metadata.topics():
            client.ensure_topic_exists(self.active_topic)

    def produce(self, event):

        future = self.producer.send(self.active_topic, event)

        if future:
            return True
        else:
            return False
