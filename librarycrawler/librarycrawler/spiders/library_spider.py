import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from librarycrawler.items import LibrarycrawlerItem  # Adjust based on where your item is defined

class LibrarySpider(CrawlSpider):
    name = "library-ensign"
    allowed_domains = ["libraryguides.ensign.edu"]
    start_urls = ["https://libraryguides.ensign.edu/"]
    handle_httpstatus_list = [200, 301, 302, 303, 307, 400, 401, 403, 404, 500]  # Add status codes you care about

    rules = (
        Rule(LinkExtractor(allow="/libraryguides/"), callback="parse_my_url", follow=True),
    )

    def parse_my_url(self, response):
        # List of HTTP status codes to report
        report_if = [
            400, 401, 402, 403, 404, 500, 501, 502, 503, 504
        ]

        if response.status in report_if:
            item = LibrarycrawlerItem()
            item['referer'] = response.request.headers.get('Referer', None)
            item['status'] = response.status
            item['response'] = response.url
            yield item

        # Optionally, handle pagination
        next_page = response.css('.next a::attr("href")').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse_my_url)

