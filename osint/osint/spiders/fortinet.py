import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import OsintItem
from ..utils.upload_minio import upload_oss
import os

class FortinetSpider(scrapy.Spider):
    name = 'fortinet'
    allowed_domains = ['www.fortinet.com/blog/threat-research']
    start_urls = ['https://www.fortinet.com/blog/threat-research']
    next_urls = ['https://www.fortinet.com/content/fortinet-blog/us/en/threat-research/jcr:content/root/bloglist.','.html']
    pages = 22

    def start_requests(self):

        for i in self.start_urls:
            # scrapy.Request()
            yield scrapy.Request(url=i, callback=self.parse, dont_filter=True)
        for i in range(0, self.pages):
            yield scrapy.Request(url = self.next_urls[0] + str(i) + self.next_urls[1],
                                 callback = self.parsenext, dont_filter = True)

    def parse(self, response):
        self.logger.info(response)
        for post in response.xpath('//div[contains(@class, "b3-blog-list__post text-container")]'):
            _source_url = post.xpath('div[1]/div[2]/h2/a/@href').extract_first()
            source_url = response.urljoin(_source_url)
            title = post.xpath('div[1]/div[2]/h2/a/text()').extract_first()
            abstract = post.xpath('div[1]/div[2]/p[2]/text()').extract_first()
            tags = ['']
            source = self.name
            publish_time = post.xpath('div[2]/div[2]/p/span[2]/text()').extract_first()
            authors = [i.strip() for i in post.xpath('div[2]/div[2]/p/span[1]/a/text()').extract()]
            item = OsintItem()
            item['title'] = title
            item['abstract'] = abstract
            item['tags'] = tags
            item['source'] = source
            item['source_url'] = source_url
            item['extract'] = {}
            item['extract']['publish_time'] = publish_time
            item['extract']['authors'] = authors
            
            yield SeleniumRequest(url=source_url, wait_time=5, callback=self.parse_content, meta={'item': item})

    def parsenext(self, response):
        self.logger.info(response)
        for post in response.xpath('//div[contains(@class, "b3-blog-list__post text-container")]'):
            _source_url = post.xpath('div[1]/div[2]/h2/a/@href').extract_first()
            source_url = response.urljoin(_source_url)
            title = post.xpath('div[1]/div[2]/h2/a/text()').extract_first()
            abstract = post.xpath('div[1]/div[2]/p[2]/text()').extract_first()
            tags = ['']
            source = self.name
            publish_time = post.xpath('div[2]/div[2]/p/span[2]/text()').extract_first()
            authors = [i.strip() for i in post.xpath('div[2]/div[2]/p/span[1]/a/text()').extract()]
            item = OsintItem()
            item['title'] = title
            item['abstract'] = abstract
            item['tags'] = tags
            item['source'] = source
            item['source_url'] = source_url
            item['extract'] = {}
            item['extract']['publish_time'] = publish_time
            item['extract']['authors'] = authors

            yield SeleniumRequest(url=source_url, wait_time=5, callback=self.parse_content, meta={'item': item})

    def parse_content(self,  response: scrapy.http.Response):
        content = response.text
        pdf_content = response.meta['driver'].print_page()
        html_path = upload_oss(content, 'fortinet')
        pdf_path = upload_oss(pdf_content, 'fortinet', file_type='pdf')
        item = response.meta['item']
        item['html_download_url'] = html_path
        item['pdf_download_url'] = pdf_path
        yield item
