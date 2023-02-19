from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3
import datetime
import os
dt_now = datetime.datetime.now()


class JobsPipeline:
    
    def open_spider(self, spider):
        # db.sqlite3と同じディレクトリに移動
        os.chdir('../')
        print("現在のディレクトリは")
        print(os.getcwd())
        
        self.connection = sqlite3.connect('db.sqlite3')
        self.c = self.connection.cursor()
        
    def process_item(self, item, spider):
        self.c.execute('''
                           INSERT INTO aggggry_app_jobs (title, job, location, price, agent, data_added, create_user_company)
                           VALUES(?, ?, ?, ?, ?, ?, ?)
                            ''',(
                                item.get('title'),
                                item.get('job'),
                                item.get('location'),
                                item.get('price'),
                                item.get('agent'),
                                item.get('data_added'),
                                item.get('create_user_company'),
                            ))
        self.connection.commit()
        return item
    
    def close_spider(self, spider):
        self.connection.close()
    