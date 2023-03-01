import scrapy
from jobs.gen_caree_item import Jobs
from scrapy.loader import ItemLoader
import datetime


class GenCareeSpider(scrapy.Spider):
    name = "gen-caree"
    allowed_domains = ["g-career.net"]
    start_urls = ["https://www.g-career.net/jobs/list?employment%5B%5D=1&parent_area%5B%5D=436&prefecture_area%5B%5D=013&city_area%5B%5D=%E6%9D%B1%E4%BA%AC23%E5%8C%BA%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B%5D=%E5%85%AB%E7%8E%8B%E5%AD%90%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B%5D=%E7%AB%8B%E5%B7%9D%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B%5D=%E6%AD%A6%E8%94%B5%E9%87%8E%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B%5D=%E5%BA%9C%E4%B8%AD%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B%5D=%E7%94%BA%E7%94%B0%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B%5D=%E6%9D%B1%E4%BA%AC%E9%83%BD%E3%80%90%E3%81%9D%E3%81%AE%E4%BB%96%E3%80%91&occupation%5B%5D=2&keyword="]

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
        if next_page == "https://www.g-career.net/jobs/list?employment%5B0%5D=1&parent_area%5B0%5D=436&prefecture_area%5B0%5D=013&city_area%5B0%5D=%E6%9D%B1%E4%BA%AC23%E5%8C%BA%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B1%5D=%E5%85%AB%E7%8E%8B%E5%AD%90%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B2%5D=%E7%AB%8B%E5%B7%9D%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B3%5D=%E6%AD%A6%E8%94%B5%E9%87%8E%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B4%5D=%E5%BA%9C%E4%B8%AD%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B5%5D=%E7%94%BA%E7%94%B0%E5%B8%82%E3%82%A8%E3%83%AA%E3%82%A2&city_area%5B6%5D=%E6%9D%B1%E4%BA%AC%E9%83%BD%E3%80%90%E3%81%9D%E3%81%AE%E4%BB%96%E3%80%91&occupation%5B0%5D=2&page=2":
        # if next_page != "#":
            yield response.follow(url=next_page, callback=self.parse)
