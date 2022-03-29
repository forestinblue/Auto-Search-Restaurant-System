# python main.pymain.py
from NewRestaurantAutoCollect import GatherNewRestaurantData
from NewRestaurantUploadFlask import run_app


if __name__ == '__main__':
    GatherNewRestaurantData.click_next_page_upload_csv()
    GatherNewRestaurantData.crawling_lat_lon_data()
    run_app()
    
    
    
    
    
    