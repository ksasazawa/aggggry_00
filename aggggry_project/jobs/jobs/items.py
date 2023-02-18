import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

def convert_yen(element):
    if element:
        return int(element.replace(',', ''))
    return 0

class Jobs(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(str.lstrip),
        output_processor = TakeFirst()
    )
    job = scrapy.Field(
        output_processor = TakeFirst()
    )
    location = scrapy.Field(
        input_processor = MapCompose(str.lstrip),
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        input_processor = MapCompose(convert_yen),
        output_processor = TakeFirst()
    )
    agent = scrapy.Field()
    data_added = scrapy.Field()
    create_user_company = scrapy.Field()
