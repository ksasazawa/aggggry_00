import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

def convert_yen(element):
    if element:
        return int(element.replace(',', ''))
    return 0

class Jobs(scrapy.Item):
    title = scrapy.Field(
        output_processor = TakeFirst()
    )
    job = scrapy.Field(
        output_processor = TakeFirst()
    )
    location = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        output_processor = TakeFirst()
    )
    agent = scrapy.Field(
        output_processor = TakeFirst()
    )
    data_added = scrapy.Field(
        output_processor = TakeFirst()
    )
    create_user_company = scrapy.Field(
        output_processor = TakeFirst()
    )
