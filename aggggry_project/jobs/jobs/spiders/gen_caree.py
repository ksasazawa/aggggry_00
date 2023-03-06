import scrapy
from jobs.gen_caree_item import Jobs
from scrapy.loader import ItemLoader
import datetime


class GenCareeSpider(scrapy.Spider):
    name = "gen-caree"
    allowed_domains = ["g-career.net"]
    start_urls = ["https://www.g-career.net/jobs/list?employment%5B%5D=1&parent_area%5B%5D=436&prefecture_area%5B%5D=013&occupation%5B%5D=2&keyword=%E6%9D%B1%E4%BA%AC"]

    # https://qiita.com/fukuyama012/items/f0121f67a3efb675c1b0
    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         "jobs.pipelines.JobsPipeline": 300,
    #     }
    # }

    def parse_item(self, response):
        loader = ItemLoader(item=Jobs(), response=response)
        loader.add_css('title', 'h1.mainTtl::text')
        loader.add_css('job', 'dl.jobInfo>div:nth-child(2)>dd::text')
        loader.add_css('location', 'dl.jobInfo>div:nth-child(1)>dd::text')
        loader.add_css('price', 'dl.jobInfo>div:nth-child(3)>dd::text')
        loader.add_value('agent', '株式会社コプロ・エンジニアード')
        loader.add_value('data_added', datetime.datetime.now())
        loader.add_value('create_user_company', '株式会社コプロ・エンジニアード')
        yield loader.load_item()
        
        # title = response.css('h1.mainTtl::text').get()
        # job = response.css('dl.jobInfo>div:nth-child(2)>dd::text').get()
        # location = response.css('dl.jobInfo>div:nth-child(1)>dd::text').get()
        # price = response.css('dl.jobInfo>div:nth-child(3)>dd::text').get()
        # yield {
        #     'title': title,
        #     'job': job,
        #     'location': location,
        #     'price': price,
        # }

    def parse(self, response):
        job_box = response.css('div.jobWrap')
        for job in job_box:
            url = job.css('div.jobIn>a::attr(href)').get()            
            yield response.follow(url=url, callback=self.parse_item)
        next_page = response.css('div.pagerBox.pcOnly>ul.pagerItems>li.pagerItem_next>a::attr(href)').get()
        if next_page and next_page != "#":
        # if next_page != "#":
            yield response.follow(url=next_page, callback=self.parse)
