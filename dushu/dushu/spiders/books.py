# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import DushuItem

from scrapy_redis.spiders import RedisCrawlSpider

class BooksSpider(RedisCrawlSpider):
    name = 'books'
    allowed_domains = ['www.dushu.com']
    # start_urls = ['https://www.dushu.com/book/1611.html']

    redis_key = 'start_urls'
    # <a href="/book/1175_2.html">2</a>
    # follow True 对新获取的页面继续使用这个规则
    # follow False 只对当前页面进行提取，当前页面就是start_urls列表中的url
    # rules = (
    #     Rule(LinkExtractor(allow=r'/book/1175_[\d]+\.html'), callback='parse_item', follow=True),
    # )
    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//dl[@class="active"]/dd'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css='div.pages > a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        books = response.xpath('//div[@class="bookslist"]/ul/li')

        for book in books:
            item = DushuItem()

            # 不会崩溃，没有数据返回None
            book_image = book.xpath('.//img/@src').extract_first('这本书没有图片')

            title = book.xpath('.//h3/a/text()').extract_first('title')

            author = book.xpath('.//p[1]/a/text()').extract_first('佚名')

            book_info = book.xpath('.//p[2]/text()').extract_first('……')

            item['title'] = title
            item['book_image'] = book_image
            item['author'] = author
            item['book_info'] = book_info

            #     目的
            yield item
