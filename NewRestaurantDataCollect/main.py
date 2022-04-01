# python main.pymain.py
from new_restaurant_auto_collect import GatherNewRestaurantData
from new_restaurant_upload_flask import run_app


if __name__ == '__main__':
    GatherNewRestaurantData.click_next_page_upload_csv()
    GatherNewRestaurantData.crawling_lat_lon_data()
    run_app()
