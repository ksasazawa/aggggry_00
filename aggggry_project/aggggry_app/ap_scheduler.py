from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
import os


def periodic_execution(): # 任意の関数名
    # ここに定期実行したい処理を記述する
    os.chdir('aggggry_project/jobs')
    os.system('scrapy crawl gen-caree')
    os.system('scrapy crawl conma')
    os.system('scrapy crawl oreyume -o oreyume.csv')
    os.chdir('../../')

# スケジュールの設定
def start():
    scheduler=BackgroundScheduler()
    scheduler.add_job(periodic_execution, 'cron', hour=17, minute=41)
    scheduler.start()


	# scheduler.add_job(
	# 	periodic_execution,
	# 	# 'interval',
	# 	# minutes=1 # 1分おきに実行する
 #    'interval',
 #    minutes=3
	# )