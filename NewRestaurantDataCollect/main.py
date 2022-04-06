from new_restaurant_upload_flask import run_app
from new_restaurant_auto_collect import GatherNewRestaurantData
from threading import Thread
import time
import schedule

data = {}


def crawl():
    print('im crawling')
    data.update(GatherNewRestaurantData.crawling_lat_lon_data())


schedule.every().wednesday.at("17:39").do(crawl)  # 월요일 00:10분에 실행


def crawl_task():
    while True:
        schedule.run_pending()
        time.sleep(1)


crawl_thread = Thread(target=crawl_task)
crawl_thread.start()

run_app(data)
crawl_thread.join()
