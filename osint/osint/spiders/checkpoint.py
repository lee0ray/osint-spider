import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import OsintItem
from ..utils.upload_minio import upload_oss


class CheckpointSpider(scrapy.Spider):
    name = "checkpoint"
    allowed_domains = ["research.checkpoint.com"]
    start_urls = ["https://research.checkpoint.com/latest-publications/"]

    def start_requests(self):
        for i in self.start_urls:
            yield scrapy.Request(url=i, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for post in response.xpath('//div[contains(@class, \'top-section-wrap\')]'):
            title = post.xpath('div/div/h3/a/text()').extract_first()
            abstract = post.xpath('p/text()').extract_first()
            source = self.name
            source_url = post.xpath('div/div/h3/a/@href').extract_first()
            publish_time = post.xpath('div[2]/div/text()').extract_first().strip()
            item = OsintItem()
            item['title'] = title
            item['abstract'] = abstract
            item['source'] = source
            item['source_url'] = source_url
            item['extract'] = {}
            item['extract']['publish_time'] = publish_time
            yield SeleniumRequest(url=source_url, wait_time=5, callback=self.parse_content, meta={'item': item})
        for post in response.xpath('//div[contains(@class, \'bottom-section-wrapper\')]'):
            title = post.xpath('div/div/h3/a/text()').extract_first()
            abstract = post.xpath('div/p/text()').extract_first()
            source = self.name
            source_url = post.xpath('div/div/h3/a/@href').extract_first()
            publish_time = post.xpath('div[1]/div/div[1]/text()').extract_first().strip()
            item = OsintItem()
            item['title'] = title
            item['abstract'] = abstract
            item['source'] = source
            item['source_url'] = source_url
            item['extract'] = {}
            item['extract']['publish_time'] = publish_time
            yield SeleniumRequest(url=source_url, wait_time=5, callback=self.parse_content, meta={'item': item})

        next_page = response.xpath('//button[@class="button background-skyblue font-white skyblue-border button-inner-link"]/a/@href').extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True)

    def parse_content(self, response: scrapy.http.Response):
        content = response.text
        pdf_content = response.meta['driver'].print_page()
        html_path = upload_oss(content, 'checkpoint')
        pdf_path = upload_oss(pdf_content, 'checkpoint', file_type='pdf')
        item = response.meta['item']
        item['html_download_url'] = html_path
        item['pdf_download_url'] = pdf_path
        yield item
