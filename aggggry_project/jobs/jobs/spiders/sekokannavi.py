import scrapy
from jobs.items import Jobs
from scrapy.loader import ItemLoader
import datetime


class SekokannaviSpider(scrapy.Spider):
    name = "sekokannavi"
    allowed_domains = ["sekokan-navi.jp"]
    start_urls = ["https://sekokan-navi.jp/searchlist/?employpattern=43&location=94&city=13209"]
    
    def parse_item(self, response):
        loader = ItemLoader(item=Jobs(), response=response)
        loader.add_css('title', 'div.area_title::text')
        loader.add_css('job', 'table.detail_table td.wysiwig>p::text')
        loader.add_css('location', 'p.location_text::text')
        loader.add_css('price', 'table.detail_table p.salary_text>span::text')
        loader.add_value('agent', 'agentA')
        loader.add_value('data_added', datetime.datetime.now())
        loader.add_value('create_user_company', 'companyA')
        yield loader.load_item()

    def parse(self, response):
        job_box = response.css('section.job_box01>div')
        for job in job_box:
            url = job.css('div.btn_detail>a::attr(href)').get()            
            yield response.follow(url=url, callback=self.parse_item)
        next_page = response.css('div.btn_next>a::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    # def parse(self, response):
    #     job_box = response.css('section.job_box01>div')
    #     for job in job_box:
    #         yield {
    #             'title': job.css('h2>a::text').get(),
    #             'job': job.css('tr:nth-child(3)>td::text').get(),
    #             'location': job.css('tr:nth-child(1)>td>p::text').get(),
    #             'price': job.css('tr:nth-child(2)>td>p>span::text').get(),
    #         }
        
