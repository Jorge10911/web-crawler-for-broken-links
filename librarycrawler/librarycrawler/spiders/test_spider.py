import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from librarycrawler.items import LibrarycrawlerItem  # Adjust based on where your item is defined

class LibrarySpider(CrawlSpider):
    name = "library-ensign"
    allowed_domains = ["libraryguides.ensign.edu"]
    start_urls = ["https://libraryguides.ensign.edu/?b=g&d=a"]
    handle_httpstatus_list = [301, 302, 303, 307, 400, 401, 403, 404, 500]  # Focus on error status codes
    report_if = [400, 401, 402, 403, 404, 500, 501, 502, 503, 504]

    rules = (
        Rule(LinkExtractor(allow="/libraryguides/"), callback="parse_start_page", follow=True), 
    )

    def parse_start_page(self, response):
        guide_links = response.css('div.s-lib-box-idx-guide-list a::attr(href)').getall()
        for link in guide_links:
            yield response.follow(link, self.parse_guide_page)
  
    def parse_guide_page(self, response):
        nav_links = response.css('div#s-lg-guide-tabs a::attr(href)').getall()
        for link in nav_links:
            yield response.follow(link, self.parse_my_url)

    def parse_my_url(self, response):
        body_links = response.css('div.content a::attr(href)').getall()
        for link in body_links:
            if link:
                full_url = response.urljoin(link)
                yield scrapy.Request(full_url, callback=self.check_link_status, errback=self.handle_error)

    def check_link_status(self, response):
        if response.status in self.report_if:
            item = LibrarycrawlerItem()
            referer = response.request.headers.get('Referer', None)
            item['referer'] = referer.decode('utf-8') if referer else 'None'
            item['status'] = response.status
            item['response'] = response.url
            yield item

    def handle_error(self, failure):
        self.logger.error(repr(failure))
        # Optionally, create an item for errors
        item = LibrarycrawlerItem()
        item['referer'] = failure.request.headers.get('Referer', None).decode('utf-8') if failure.request.headers.get('Referer', None) else 'None'
        item['status'] = failure.value.response.status if failure.value.response else 'N/A'
        item['response'] = failure.request.url
        yield item
        To run your Scrapy spider, follow these steps:

1. **Install Scrapy**:
   If you haven't already, install Scrapy using pip:
   ```bash
   pip install scrapy
   ```

2. **Create a Scrapy Project**:
   If you don't have a Scrapy project set up, create one by running:
   ```bash
   scrapy startproject librarycrawler
   ```
   This will create a directory structure for your project.

3. **Add Your Spider**:
   Save your spider code in a file within the `spiders` directory of your Scrapy project. For example, you might save it as `library_spider.py`:
   ```
   librarycrawler/
       scrapy.cfg
       librarycrawler/
           __init__.py
           items.py
           middlewares.py
           pipelines.py
           settings.py
           spiders/
               __init__.py
               library_spider.py  # Your spider file
   ```

4. **Define Your Item**:
   Ensure that `LibrarycrawlerItem` is defined in `items.py`:
   ```python
   import scrapy

   class LibrarycrawlerItem(scrapy.Item):
       referer = scrapy.Field()
       status = scrapy.Field()
       response = scrapy.Field()
   ```

5. **Run Your Spider**:
   Navigate to your project directory and run your spider using the following command:
   ```bash
   scrapy crawl library-ensign
   ```

This command will start the crawling process, and you should see the output in your terminal. If you encounter any issues, check the error messages for clues on what might be going wrong. Feel free to share any specific errors you encounter, and I can help troubleshoot them!