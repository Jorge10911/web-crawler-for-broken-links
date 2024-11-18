from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class LibarySpider(CrawlSpider):
    name = "library-ensign"
    allowed_domains = ["library.ensign.edu","libraryguides.ensign.edu"]
    start_urls = ["https://library.ensign.edu/"] # list of starting urls for the crawler
    handle_httpstatus_list = [200, 301, 302, 303, 307, 400, 401, 403, 404, 500] # only 200 by default. you can add more status to list

    rules = (
        Rule(LinkExtractor(allow="/libraryguides/"))
        Rule(LinkExtractor(allow="" deny="" callback="parse_my_url"))

    )

    def parse_my_url(self, response):
        report_if =[
        400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 425, 426, 428, 429, 431, 451,
        500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511 
        ]#list of responses that we want to include on the report,

        if response.status in report_if: # if the response matches then creates a MyItem
            item = MyItems()
            item['referer'] = response.request.headers.get('Referer', None)
            item['status'] = response.status
            item['response']= response.url
            yield item
        yield None # if the response did not match return empty