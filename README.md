# DataPipleLine-opening/closed Restaurant data
## Introduce 
> Every day, Many restaurants open or close.

I needed to develope automatically searchng open/closed Restaurants System to update DB's restaurant data.

There are two kind of Systems.

One is searching new restaurant system,
the other is searching closed's.

## Crawling-1
Scrap this [Site](http://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoCompany.do?menu_grp=MENU_NEW04&menu_no=2813)

There are informations which is  recently new/closed retaurant's name and new address.

<img src="https://user-images.githubusercontent.com/90318043/158913663-7d40097c-2595-4f0d-8515-d8a395f8c57e.png" width="750" height="400"/>

## Crawling-2

We can find  new/closed retaurant's lattitude & longtitude and old_address with this [site](https://address.dawul.co.kr/index.php)

<img src="https://user-images.githubusercontent.com/90318043/158917598-fb4b0934-278d-4717-adcd-f35004708ffa.png" width="750" height="400"/>

## Upload data in server, Flask
To Update DataBase with new/closed restautant data, i upload data into web using Flask.

```python
from flask import Flask, jsonify
app =  Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route("/")
def test_json():
    return jsonify(foodsafetykorea_closed_information.to_dict('records'))
if __name__ == "__main__":
    app.run()
```

## Schedule Modulization
In Window system, There is no availble for use with Contrab Python library.

So, I use [Schedule Module](https://github.com/dbader/schedule) made by other python user.
```python
import time
import schedule
import sys 
from NewRestaurantDataCollect import main

def data_collect():
    main.main()
 
 
schedule.every().tuesday.at("10:25").do(data_collect) #화요일 10새:25분에 실행

#실제 실행하게 하는 코드
while True:
    schedule.run_pending()
    time.sleep(1)
```

## Threading
While I will turn on the server, crawling food-information-websites. 

I use [Thread](https://haerong22.tistory.com/39) library in Python.
```python
from threading import Thread
import time
import schedule


data = []


def crawl():
    print('im crawling')
    GatherNewRestaurantData.click_next_page_upload_csv()
    GatherNewRestaurantData.crawling_lat_lon_data()


schedule.every().tuesday.at("13:53").do(crawl)  # 월요일 00:10분에 실행
# schedule.every().day.at("10:30").do(job) #매일 10시30분에


def crawl_task():
    while True:
        schedule.run_pending()
        time.sleep(1)


crawl_thread = Thread(target=crawl_task)
crawl_thread.start()

run_app()
crawl_thread.join()
```






