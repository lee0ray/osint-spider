# Scrapy settings for osint project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from shutil import which

BOT_NAME = "osint"

SPIDER_MODULES = ["osint.spiders"]
NEWSPIDER_MODULE = "osint.spiders"


# SCHEDULER = "scrapy_distributed.schedulers.DistributedScheduler"
# SCHEDULER_QUEUE_CLASS = "scrapy_distributed.queues.kafka.KafkaQueue"
KAFKA_CONNECTION_PARAMETERS = "111.202.72.197:39092"
KAFKA_USERNAME = 'kafAdmin'
KAFKA_PASSWORD = 'A?5#Pkn3Smudnicn'
# DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# BLOOM_DUPEFILTER_REDIS_URL = "redis://:@localhost:6379/0"
# BLOOM_DUPEFILTER_REDIS_HOST = "localhost"
# BLOOM_DUPEFILTER_REDIS_PORT = 6379
# REDIS_BLOOM_PARAMS = {"redis_cls": "redisbloom.client.Client"}
# BLOOM_DUPEFILTER_ERROR_RATE = 0.001
# BLOOM_DUPEFILTER_CAPACITY = 100_0000
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
REDIS_URL = 'redis://redis:6379'

# Number of Hash Functions to use, defaults to 6
BLOOMFILTER_HASH_NUMBER = 6

# Redis Memory Bit of Bloom Filter Usage, 30 means 2^30 = 128MB, defaults to 30
BLOOMFILTER_BIT = 30

# Persist
SCHEDULER_PERSIST = True


SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which(r'chromedriver')
SELENIUM_DRIVER_ARGUMENTS = ['--disable-dev-shm-usage',
                             '--no-sandbox',
                             '--disable-gpu',
                             # '--single-process',
                             '--log-level=0',
                             '--window-size=1920,1080',
                             '--headless',
                             '--disable-infobars',
                             ]
SELENIUM_MIN_DRIVERS = 5
SELENIUM_MAX_DRIVERS = 10


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "osint (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "osint.middlewares.OsintSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # "osint.middlewares.OsintDownloaderMiddleware": 543,
    # "scrapy_distributed.middlewares.kafka.KafkaMiddleware": 542,
    'scrapy_selenium.SeleniumMiddleware': 800
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "osint.pipelines.OsintPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

OSS_ENDPOINT_PATH = 'minio:9000'
OSS_ACCESS_KEY = 'DJQYbEOzgwu1s45BGfxH'
OSS_SECRET_KEY = 'l06tZxXDz81mVGtTUVSkqaWWcRMWzFTOaiwmHMMy'
OSS_BUCKET = 'osint-spider'
OSS_ARGS = {'secure': False}
