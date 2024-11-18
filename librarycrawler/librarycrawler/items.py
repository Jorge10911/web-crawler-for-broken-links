# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
import scrapy


class LibrarycrawlerItem(Item):
    referer =Field() # where the link is extracted
    response = Field() # url that was requested
    status = Field()
