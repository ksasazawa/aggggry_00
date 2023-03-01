import scrapy
from jobs.kyodo_item import Jobs
from scrapy.loader import ItemLoader
import datetime


class KyodoSpider(scrapy.Spider):
    name = "kyodo"
    allowed_domains = ["recruit.kyodo-engine.com"]
    start_urls = ["https://recruit.kyodo-engine.com/career/job/?area=tokyo&type1=01&type2=01&s"]

    def parse_item(self, response):
        title = response.css('h3.title::text').get()
        rows = response.css("table.job-table tr")
        for i, r in enumerate(rows.extract()):
            if '<th>業種</th>' in r:
                gyoshu_no = i+1
                print(f"ghoshu_no:{gyoshu_no}")
                gyoshu = response.css(f'table.job-table tr:nth-child({gyoshu_no})>td::text').get()
            if '<th>職種</th>' in r:
                job_no = i+1
                print(f"job_no:{job_no}")
                job = response.css(f'table.job-table tr:nth-child({job_no})>td::text').get()
            elif '<th>勤務地</th>' in r:
                location_no = i+1
                print(f"location_no:{location_no}")
            elif '<th>給与</th>' in r:
                price_no = i+1
        loader = ItemLoader(item=Jobs(), response=response)
        loader.add_css('title', 'h3.title::text')
        loader.add_value('job', gyoshu+job)
        loader.add_css('location', f'table.job-table tr:nth-child({location_no})>td::text')
        loader.add_css('price', f'table.job-table tr:nth-child({price_no})>td::text')
        loader.add_value('agent', '共同エンジニアリング株式会社')
        loader.add_value('data_added', datetime.datetime.now())
        loader.add_value('create_user_company', '共同エンジニアリング株式会社')
        yield loader.load_item()

    def parse(self, response):
        job_box = response.css('div.job-box')
        for job in job_box:
            url = job.css('li.job-btn_more>a::attr(href)').get()       
            yield response.follow(url=url, callback=self.parse_item)
        next_page = response.css('a.nextpostslink::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
