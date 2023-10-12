import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import OsintItem
from ..utils.upload_minio import upload_oss


class TalosintelligenceSpider(scrapy.Spider):
    name = 'talosintelligence'
    allowed_domains = ['blog.talosintelligence.com']
    start_urls = ['https://blog.talosintelligence.com/']

    def start_requests(self):
        for i in self.start_urls:
            # scrapy.Request()
            yield scrapy.Request(url=i, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print('-----------------------',response.urljoin)
        for post in response.xpath('//div[contains(@class, "post-wrapper")]'):
            title = post.xpath('div/div/div/h2/a/text()').extract_first()
            abstract = post.xpath('div/div/div/p/text()').extract_first()
            tags = [i.strip() for i in post.xpath('div/div/div/div[contains(@class, "tags-block")]/a/text()').extract()]
            source = self.name
            _source_url = post.xpath('div/div/div/h2/a/@href').extract_first()
            source_url = response.urljoin(_source_url)
            publish_time = post.xpath('div/div/div/span/text()').extract_first()
            if not publish_time:
                publish_time = response.xpath('//*[@id="site-main"]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div/div[2]').extract_first()
            authors = [i.strip() for i in post.xpath('div/div/div/div[contains(@class, "authors-block")]/a/text()').extract()]
            item = OsintItem()
            item['title'] = title
            item['abstract'] = abstract
            item['tags'] = tags
            item['source'] = source
            item['source_url'] = source_url
            item['extract'] = {}
            item['extract']['publish_time'] = publish_time
            item['extract']['authors'] = authors
            # print('item',item)
            yield SeleniumRequest(url=source_url, wait_time=5, callback=self.parse_content, meta={'item': item})
        _next_page_url = response.xpath('//*[@id="site-main"]/div/div/div/div/div/div/div/div/div/nav/a')[-1]
        print('_next_page_url----------------------------------',_next_page_url)
        if 'Next' in _next_page_url.xpath('text()').extract_first():
            next_page_url = response.urljoin(_next_page_url.xpath('@href').extract_first())
            print('next_page_url----------------------------------',next_page_url)
            yield scrapy.Request(url=next_page_url, )

    def parse_content(self,  response: scrapy.http.Response):
        print('response.url=====================================',response.url)
        content = response.text
        pdf_content = response.meta['driver'].print_page()

        item = response.meta['item']

        # html_path = upload_oss(content, 'talosintelligence')
        # pdf_path = upload_oss(pdf_content, 'talosintelligence', file_type='pdf')
        #
        # item['html_download_url'] = html_path
        # item['pdf_download_url'] = pdf_path
        yield item
