import scrapy
from jobs.conma_item import Jobs
from scrapy.loader import ItemLoader
import datetime


class ConmaSpider(scrapy.Spider):
    name = "conma"
    allowed_domains = ["conma.jp"]
    start_urls = ["https://conma.jp/zenkoku/PC13/MC1"]

    def parse_item(self, response):
        rows = response.css("table#w0 tr")
        for i, r in enumerate(rows.extract()):
            if '<th>職種</th>' in r:
                job_no = i+1
            elif '<th>勤務地</th>' in r:
                location_no = i+1
            elif '<th>給与</th>' in r:
                price_no = i+1
        loader = ItemLoader(item=Jobs(), response=response)
        loader.add_css('title', 'h1.resultTitle::text')
        loader.add_css('job', f'table#w0 tr:nth-child({job_no})>td::text')
        loader.add_css('location', f'table#w0 tr:nth-child({location_no})>td::text')
        loader.add_css('price', f'table#w0 tr:nth-child({price_no})>td::text')
        loader.add_value('agent', '株式会社アーキ・ジャパン')
        loader.add_value('data_added', datetime.datetime.now())
        loader.add_value('create_user_company', '株式会社アーキ・ジャパン')
        yield loader.load_item()
        
        # rows = response.css("table#w0 tr")
        # for row in rows:
        #     loader = ItemLoader(item=Jobs(), selector=row)
        #     th = row.css("th::text").get()
        #     if th == "職種":
        #         loader.add_css('job', 'td::text')
        #     elif th == "勤務地":
        #         loader.add_css('location', 'td::text')
        #     elif th == "給与":
        #         loader.add_css('price', 'td::text')
        
        # yield loader.load_item()
        
        # title = response.css('h1.resultTitle::text').get()
        # rows = response.css("table#w0 tr")            
        # for row in rows:
        #     th = row.css("th::text").get()
        #     if th == "職種":
        #         job = row.css("td::text").get()
        #     elif th == "勤務地":
        #         location = row.css("td::text").get()
        #     elif th == "給与":
        #         price = row.css("td::text").get()
        # yield {
        #     'title': title,
        #     'job': job,
        #     'location': location,
        #     'price': price
        # }

    def parse(self, response):
        job_box = response.css('div.mod-jobResultBox')
        for job in job_box:
            url = job.css('div.btn-group>div.btn-group__right.hide-sp>a::attr(href)').get()       
            yield response.follow(url=url, callback=self.parse_item)
        next_page = response.css('li.next>a::attr(href)').get()
        if next_page == '/zenkoku/PC13/MC1?page=2':
            yield response.follow(url=next_page, callback=self.parse)
