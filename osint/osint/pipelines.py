# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kafka import KafkaProducer
from .settings import KAFKA_CONNECTION_PARAMETERS, KAFKA_USERNAME, KAFKA_PASSWORD
import json


class OsintPipeline:
    def __init__(self):
        self.producer = None

    def open_spider(self, spider):
        self.producer = KafkaProducer(bootstrap_servers=[KAFKA_CONNECTION_PARAMETERS], batch_size=500,
                                      sasl_mechanism='PLAIN',
                                      sasl_plain_username=KAFKA_USERNAME,
                                      sasl_plain_password=KAFKA_PASSWORD,
                                      security_protocol='SASL_PLAINTEXT',
                                      linger_ms=1000,
                                      api_version=(0, 9, 0))

    def close_spider(self, spider):
        self.producer.close()

    def process_item(self, item, spider):
        self.producer.send('lt.ti.osint', key=None, value=json.dumps(dict(item)).encode('utf-8'))
        return item
