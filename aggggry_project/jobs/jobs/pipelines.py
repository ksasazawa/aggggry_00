from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3
import datetime
import os
import time
dt_now = datetime.datetime.now()


class JobsPipeline:
    def __init__(self):
        self.item_list = []

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
            time.sleep(10)
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

        if spider.name == "sekokannavi":
            self.connection = sqlite3.connect('db.sqlite3')
            self.c = self.connection.cursor()
            self.c.execute('''
                            DELETE FROM aggggry_app_jobs WHERE agent = '株式会社ウィルオブ・コンストラクション'
                                ''')
            self.connection.commit()

        if spider.name == "oreyume":
            self.connection = sqlite3.connect('db.sqlite3')
            self.c = self.connection.cursor()
            self.c.execute('''
                            DELETE FROM aggggry_app_jobs WHERE agent = '株式会社夢真'
                                ''')
            self.connection.commit()
        
    def process_item(self, item, spider):
        if item['title'] in self.item_list:
            print("重複しているよ！")
            raise DropItem("Duplicate item found: %s" % item)
        else:
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
        self.c.execute('''DELETE FROM aggggry_app_jobs WHERE id NOT IN (SELECT MIN(id) FROM aggggry_app_jobs GROUP BY title, job, location, price, agent)''')
        self.connection.commit()
        self.connection.close()
    