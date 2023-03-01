import scrapy
from jobs.items import Jobs
from scrapy.loader import ItemLoader
import datetime
import logging

class SekokanNextSpider(scrapy.Spider):
    name = "sekokan-next"
    allowed_domains = ["sekokan-next.worldcorp-jp.com"]
    start_urls = ["https://sekokan-next.worldcorp-jp.com/pref/PC13/MC1"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            })

    def parse_item(self, response):
        rows = response.css("table#w0 tr")
        for row in rows:
            th = row.css("th::text").get()
            if th == "職種名":
                title = row.css("td::text").get()
            elif th == "給与":
                price = row.css("td::text").get()
        yield {
            'title': title,
            'price': price
        }

    def parse(self, response):
        logging.info(response.request.headers['User-Agent'])
        job_box = response.css('mod-jobResultBox-wrap')
        for job in job_box:
            url = job.css('div.btn-group>div.btn-group__right.hide-sp>a::attr(href)').get()            
            yield response.follow(url=url, callback=self.parse_item)
        # next_page = response.css('div.btn_next>a::attr(href)').get()
        # if next_page:
        #     yield response.follow(url=next_page, callback=self.parse)
