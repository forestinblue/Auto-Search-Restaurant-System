# Auto-Search-Restaurant-System
## Introduce 
> Every day, Many restaurants open or close.

I needed to develope automatically searchng open/closed Restaurants System to update DB's restaurant data.

There are two kind of Systems.

One is searching new restaurant system,
the other is searching closed's.

## Work Flow-1
Scrap this [Site](http://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoCompany.do?menu_grp=MENU_NEW04&menu_no=2813)

There are informations which is  recently new/closed retaurant's name and new address.

<img src="https://user-images.githubusercontent.com/90318043/158913663-7d40097c-2595-4f0d-8515-d8a395f8c57e.png" width="750" height="400"/>

## 2

We can find  new/closed retaurant's lattitude & longtitude and old_address with this [site](https://address.dawul.co.kr/index.php)

<img src="https://user-images.githubusercontent.com/90318043/158917598-fb4b0934-278d-4717-adcd-f35004708ffa.png" width="750" height="400"/>

## 3
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

## 4
Use [CronTab](https://pypi.org/project/python-crontab/) in Python library
