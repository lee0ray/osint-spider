import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import OsintItem
from ..utils.upload_minio import upload_oss
import os


class InfosecurityMagazineSpider(scrapy.Spider):
    name = 'infosecuritymagazine'
    allowed_domains = ['www.infosecurity-magazine.com']
    start_urls = ['https://www.infosecurity-magazine.com/news/']

    def start_requests(self):
        for i in self.start_urls:
            # scrapy.Request()
            yield scrapy.Request(url=i, callback=self.parse, dont_filter=True)

    def parse(self, response):
        self.logger.info(response)
        for post in response.xpath('//div[contains(@class, "webpage-info")]'):
            _source_url = post.xpath('h2/a/@href').extract_first()
            source_url = response.urljoin(_source_url)
            
            title = post.xpath('h2/a/text()').extract_first()
            abstract = post.xpath('p/text()').extract_first()
            tags = ['']
            source = self.name
            publish_time = post.xpath('span/time/text()').extract_first()
            authors =['']
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
            
        _next_page_url = response.xpath('//div[contains(@class, "pagination")]/a')[-1]
        if 'Older' in _next_page_url.xpath('text()').extract_first():
            next_page_url = response.urljoin(_next_page_url.xpath('@href').extract_first())

            yield scrapy.Request(url=next_page_url, )

    def parse_content(self,  response: scrapy.http.Response):
        content = response.text
        pdf_content = response.meta['driver'].print_page()
        html_path = upload_oss(content, 'infosecuritymagazine')
        pdf_path = upload_oss(pdf_content, 'infosecuritymagazine', file_type='pdf')
        item = response.meta['item']
        item['html_download_url'] = html_path
        item['pdf_download_url'] = pdf_path
        yield item

