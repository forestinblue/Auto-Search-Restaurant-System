
from closed_restaurant_auto_collect import GatherClosedRestaurantData
from closed_restaurant_upload_flask import run_app


if __name__ == '__main__':
    GatherClosedRestaurantData.click_next_page_upload_csv()
    GatherClosedRestaurantData.crawling_lat_lon_data()
    run_app()
