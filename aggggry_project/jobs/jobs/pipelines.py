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
        print(f"現在のディレクトリは{os.getcwd()}")
        
        if spider.name == "gen-caree":
            self.connection = sqlite3.connect('db.sqlite3')
            self.c = self.connection.cursor()
            self.c.execute('''
                            DELETE FROM aggggry_app_jobs WHERE agent = '株式会社コプロ・エンジニアード'
                                ''')
            self.connection.commit()
            
        if spider.name == "conma":
            self.connection = sqlite3.connect('db.sqlite3')
            self.c = self.connection.cursor()
            self.c.execute('''
                            DELETE FROM aggggry_app_jobs WHERE agent = '株式会社アーキ・ジャパン'
                                ''')
            self.connection.commit()
            
        if spider.name == "kyodo":
            self.connection = sqlite3.connect('db.sqlite3')
            self.c = self.connection.cursor()
            self.c.execute('''
                            DELETE FROM aggggry_app_jobs WHERE agent = '共同エンジニアリング株式会社'
                                ''')
            self.connection.commit()
        
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
    