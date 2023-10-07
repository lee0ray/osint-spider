import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import OsintItem
from ..utils.upload_minio import upload_oss
import os

class ZscalerSpider(scrapy.Spider):
    name = 'zscaler'
    allowed_domains = ['www.zscaler.com']
    start_urls = ['https://www.zscaler.com/blogs?type=security-research']


    def start_requests(self):

        '''！！！！！！！！！！！！！！！！！！！！！！！！
        被设置了反爬,只能爬取top滑动文章
        response.xpath('/html/body/div[1]/div/div/main/div[2]/div/div/div/div[3]/div[2]/h2/text()')
        response.xpath('/html/body/div[1]/div/div/main/div[6]/div/div[2]/div[3]/div/div[2]/h3/text()')
        '''
        # for i in self.start_urls:
        #     # scrapy.Request()
        #     yield scrapy.Request(url=i, callback=self.parse_top, dont_filter=True)
        #     yield scrapy.Request(url=i, callback=self.parse, dont_filter=True)
            
    def parse_top(self, response):
        self.logger.info(response)
        top_post_left = response.xpath('//div[contains(@class, "mainContainer")]')
        _source_url = top_post_left.xpath('/html/body/div[1]/div/div/main/div[2]/div/div/div/div[2]/div[2]/div[3]/div[2]/a/@href').extract_first()
        source_url = response.urljoin(_source_url)
        
        title = top_post_left.xpath('div[2]/div[2]/h2/text()').extract_first()
        abstract = top_post_left.xpath('div[2]/div[2]/div[2]/text()').extract_first()
        tags = top_post_left.xpath('div[2]/div[2]/div[1]/div[1]/text()').extract_first()
        source = self.name
        publish_time = top_post_left.xpath('div[2]/div[2]/div[1]/div[2]/div[1]/text()').extract_first()
        authors = [i.strip() for i in top_post_left.xpath('div[2]/div[2]/div[3]/div[1]/div[2]/text()').extract()]
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
            
    def parse(self, response):
        self.logger.info(response)
        for post in response.xpath('//div[contains(@class, teaserCard_card__rpoBD)]')[:2]:
            _source_url = post.xpath('div[2]/div[3]/div/div[2]/a/@href').extract_first()
            source_url = response.urljoin(_source_url)
            
            title = post.xpath('div[2]/div[3]/div/div[2]/h3/text()').extract_first()
            abstract = ['']
            tags = post.xpath('div[2]/div[3]/div/div[2]/p/text()').extract_first()
            source = self.name
            publish_time = post.xpath('div[2]/div[3]/div/div[2]/div[2]/div[2]/div[2]/text()').extract_first()
            authors = [i.strip() for i in post.xpath('div[2]/div[3]/div/div[2]/div[2]/div[2]/div[1]/text()').extract()]
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
        html_path = upload_oss(content, 'zscaler')
        pdf_path = upload_oss(pdf_content, 'zscaler', file_type='pdf')
        item = response.meta['item']
        item['html_download_url'] = html_path
        item['pdf_download_url'] = pdf_path
        yield item

