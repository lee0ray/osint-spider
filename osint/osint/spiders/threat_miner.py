import scrapy
from scrapy_selenium import SeleniumRequest


class ThreatMinerSpider(scrapy.Spider):
    name = "threat_miner"
    allowed_domains = ["threatminer.org", 'www.threatminer.org']
    start_urls = ["https://threatminer.org"]

    def start_requests(self):
        for i in self.start_urls:
            # scrapy.Request()
            yield SeleniumRequest(url=i, wait_time=5, callback=self.parse)

    def parse(self, response):
        self.logger.info(response)
        # print(response)
        input()
