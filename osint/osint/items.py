# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OsintItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    tags = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    html_download_url = scrapy.Field()
    pdf_download_url = scrapy.Field()
    extract = scrapy.Field()
    crawling_time = scrapy.Field()
