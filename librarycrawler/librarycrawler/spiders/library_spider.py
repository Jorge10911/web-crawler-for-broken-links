import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from librarycrawler.items import LibrarycrawlerItem  # Adjust based on where your item is defined

class LibrarySpider(CrawlSpider):
    name = "library-ensign"
    allowed_domains = ["libraryguides.ensign.edu"]
    start_urls = ["https://libraryguides.ensign.edu/?b=g&d=a"]
    handle_httpstatus_list = [200, 301, 302, 303, 307, 400, 401, 403, 404, 500]  # Add status codes you care about
    report_if = [400, 401, 402, 403, 404, 500, 501, 502, 503, 504]

    rules = (
        Rule(LinkExtractor(allow="/libraryguides/"), callback="parse_start_page", follow=True), 
    )

    def parse_start_page(self, response):
        guide_links = response.css('div.s-lib-box-idx-guide-list a::attr("href")').getall()
        for link in guide_links:
            yield response.follow(link, self.parse_guide_page)
  
    def parse_guide_page(self, response):
        nav_links = response.css('div#s-lg-guide-tabs a::attr("href")').getall()
        for link in nav_links:
            yield response.follow(link, self.parse_my_url)

    def parse_my_url(self, response):
        body_links = response.css('div.content a::attr("href")').getall()
        for link in body_links:
            if link:
                full_url = response.urljoin(link)
                yield scrapy.Request(full_url, callback=self.check_link_status, errback=self.handle_error)

    def check_link_status(self, response):
        if response.status in self.report_if:
            item = LibrarycrawlerItem()
            item['referer'] = response.request.headers.get('Referer', None).decode('utf-8')
            item['status'] = response.status
            item['response'] = response.url
            yield item

    def handle_error(self, failure):
        self.logger.error(repr(failure))