from NewRestaurantAutoCollect import GatherNewRestaurantData
from NewRestaurantUploadFlask import uploadFlask


if __name__ == '__main__':
    GatherNewRestaurantData.crawling_new_restaurant_data()
    GatherNewRestaurantData.crawling_lat_lon_data()
    uploadFlask.upload_json()