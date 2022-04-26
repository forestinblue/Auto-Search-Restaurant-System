from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time as time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_seq_items', 100)

# 새로운 식당 정보 crawling
# crawling 순서: 식품안전나라(식당이름, 도로명주소, 인허가번호, 인덱스 번호 )수집 -> 다올 주소변환(지번주소, 위도, 경도 , 우편번호) 수집
# function flow: crawling_lat_lon_data -> click_next_page_upload_csv -> open_driver_new_restaurant_site -> clear_restaurant_dataframe -> crawling_new_restaurant_data -> open_driver_lat_lon_site


class GatherClosedRestaurantData:
    global capa
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    global options
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--incognito")
    options.add_argument('--window-size=1920x1080')
    global collected_license_number
    print('write collected_license_number')
    collected_license_number = input()  # 마지막으로 수집한 식당 인허가번호

    # open 식품안전나라

    def open_driver_closed_restaurant_site():
        print('open_driver_closed_restaurant_site')
        global driver
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        driver.get(
            "http://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoCompany.do?menu_grp=MENU_NEW04&menu_no=2813")  # 식품나라안전 사이트
        driver.maximize_window()
        time.sleep(5)
        driver.find_element_by_xpath(
            '//*[@id="mode1"]/div[1]/div[1]/ul/li[4]/a').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="opt6_2_1"]').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="srchBtn"]').click()
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="sp_list_cnt"]').click()
        time.sleep(10)
        driver.find_element_by_xpath(
            '//*[@id="contents"]/main/section/div[2]/div[2]/div[3]/div/ul/li[5]/a').click()
        time.sleep(10)

     # 식품나라안전 page crawling
    def crawling_closed_restaurant_data():
        print('crawling_new_restaurant_data')
        closed_restaurant_information = GatherClosedRestaurantData.clear_restaurant_dataframe()
        time.sleep(10)
        return_dataframe = pd.DataFrame(columns=['name', 'license_number', 'old_address',
                                                 'new_address', 'zip_code', 'latitude', 'longtitude', 'index_number'])
        except_name_list = ['씨유', 'CU', 'cu', '세븐일레븐', '이마트24', 'GS25',
                            '지에스25', 'GS', '보드게임', '보드카페', '보드까페', '장례', '마트', 'PC', 'pc', '유통']

        for n in range(1, 50, 1):
            time.sleep(0.1)
            if driver.find_elements_by_css_selector(f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(4) > span.table_txt')[0].text == '위탁급식영업' or driver.find_elements_by_css_selector(f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(4) > span.table_txt')[0].text == '집단급식소':
                pass
            else:
                n_index_number = driver.find_elements_by_css_selector(
                    f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(1) > span.table_txt')[0].text
                n_license_number = driver.find_elements_by_css_selector(
                    f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(2) > span.table_txt')[0].text
                n_name = driver.find_elements_by_css_selector(
                    f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(3) > span.table_txt')[0].text
                n_new_address = driver.find_elements_by_css_selector(
                    f'#tbl_bsn_list > tbody > tr:nth-child({n}n) > td:nth-child(6) > span.table_txt')[0].text

                if n_license_number == collected_license_number:
                    return_dataframe = closed_restaurant_information
                    quit = 1  # 마지막으로 수집한 식당 인허가번호가 나오면 quit = 1 -> stop crawling
                    break

                n_old_address = ''
                n_zip_code = ''
                n_longtitude = ''
                n_latitude = ''

                append_judgement = True
                # except_name_list 제외환  나머지 항목은 append flow 만들기
                for i in range(len(except_name_list)):

                    if except_name_list[i] == n_name:
                        append_judgement = False
                if append_judgement == True:
                    closed_restaurant_information = closed_restaurant_information.append({'name': n_name,  'new_address': n_new_address, 'old_address': n_old_address,  'zip_code': n_zip_code, 'license_number': n_license_number,
                                                                                          'index_number': n_index_number, 'latitude': n_latitude, 'longtitude': n_longtitude}, ignore_index=True)

                print(n_index_number)
                print(n_license_number)
                print(n_name)
                print(n_old_address)
                n_index_number = ''
                n_license_number = ''
                n_name = ''
                n_new_address = ''
            return_dataframe = closed_restaurant_information
            quit = 0
        return quit, return_dataframe

    # new-dataframe 만들기
    def clear_restaurant_dataframe():
        new_dataframe = pd.DataFrame(columns=['name', 'license_number', 'old_address',
                                     'new_address', 'zip_code', 'latitude', 'longtitude', 'index_number'])
        return(new_dataframe)

    # 식품나라안전 click next page
    def click_next_page_upload_csv():
        GatherClosedRestaurantData.open_driver_closed_restaurant_site()  # open 식품나라안전

        page_count = 0
        # assign new-dataframe
        foodsafetykorea_closed_restaurant_information = GatherClosedRestaurantData.clear_restaurant_dataframe()

        quit = 0
        while quit == 0:  # quit = 0이면 while 반복 ,  quit = 1이면 break while
            page_count += 1
            print('page_count ={}'.format(page_count))  # 식품안전나라 page
            # 식품안전나라 page crawling
            quit, crawling_dataframe = GatherClosedRestaurantData.crawling_closed_restaurant_data()
            foodsafetykorea_closed_restaurant_information = foodsafetykorea_closed_restaurant_information.append(
                crawling_dataframe)
            driver.find_element_by_css_selector(
                '#contents > main > section > div.board-footer > div > ul > li:nth-child(7) > a').click()  # 식품안전나라 next page click
            time.sleep(2)
        print('finish crawling new restaurant data')
        foodsafetykorea_closed_restaurant_information = foodsafetykorea_closed_restaurant_information.reset_index(
            drop=True)
        return foodsafetykorea_closed_restaurant_information

    def open_driver_lat_lon_site():
        print('start adding lattitude and longtitude data')
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install(
        ), desired_capabilities=capa,  chrome_options=options)
        wait = WebDriverWait(driver, 3)
        driver.get("https://address.dawul.co.kr/index.php")
        time.sleep(2)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#addrProRs')))
        time.sleep(1)
        driver.execute_script("window.stop();")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])  # 팝업창을 선택
        time.sleep(0.5)
        driver.close()  # 팝업창 삭제
        time.sleep(0.5)
        driver.switch_to.window(driver.window_handles[0])  # main창 선택
        time.sleep(0.5)

    def crawling_lat_lon_data():
        # 식품나라안전 crawling한 dataframe값 return
        foodsafetykorea_closed_restaurant_information = GatherClosedRestaurantData.click_next_page_upload_csv()
        GatherClosedRestaurantData.open_driver_lat_lon_site()  # open 위도경도변환site, Dawul주소변환
        time.sleep(3)
        foodsafetykorea_closed_restaurant_information = foodsafetykorea_closed_restaurant_information.reset_index(
            drop=True)  # key_error 방지
        foodsafetykorea_closed_restaurant_address = list(
            foodsafetykorea_closed_restaurant_information['new_address'])  # 도로명주소로 검색
        search_box = driver.find_element(By.NAME, "juso")  # 검색창
        for i in range(len(foodsafetykorea_closed_restaurant_information)):
            while True:
                search_box.clear()
                try:
                    search_box.send_keys(
                        foodsafetykorea_closed_restaurant_address[i])
                    search_box.send_keys(Keys.RETURN)  # 검색창 입력
                except:
                    break
                time.sleep(1.5)
                try:  # 지번 주소 등록
                    foodsafetykorea_closed_restaurant_information['old_address'][i] = driver.find_elements_by_css_selector(
                        '#insert_data_3 ')[0].text
                except Exception as e:
                    print(e)
                    foodsafetykorea_closed_restaurant_information['old_address'][i] = ''
                try:  # 우편 주소 등록
                    foodsafetykorea_closed_restaurant_information['zip_code'][i] = driver.find_elements_by_css_selector(
                        '#insert_data_4')[0].text
                except Exception as e:
                    print(e)
                    foodsafetykorea_closed_restaurant_information['zip_code'][i] = ''
                n_lat_lon = driver.find_elements_by_css_selector('#insert_data_5')[
                    0].text  # 위도경도 문자열 나누기
                n_lon = n_lat_lon.split(',')[0]
                n_lat = n_lat_lon.split(',')[1]
                n_lon = n_lon[3:]
                n_lat = n_lat[4:]
                print()

                try:  # 위도 등록
                    foodsafetykorea_closed_restaurant_information['latitude'][i] = n_lat
                except Exception as e:
                    print(e)
                    foodsafetykorea_closed_restaurant_information['latitude'][i] = ''
                try:  # 경도 등록
                    foodsafetykorea_closed_restaurant_information['longtitude'][i] = n_lon
                except Exception as e:
                    print(e)
                    foodsafetykorea_closed_restaurant_information['longtitude'][i] = ''

                print(
                    foodsafetykorea_closed_restaurant_information['old_address'][i])
                print(
                    foodsafetykorea_closed_restaurant_information['zip_code'][i])
                print(
                    foodsafetykorea_closed_restaurant_information['latitude'][i])
                print(
                    foodsafetykorea_closed_restaurant_information['longtitude'][i])

                n_lat_lon = ''
                n_lat = ''
                n_lon = ''
                break
            # dataframe -> dict 전환
            foodsafetykorea_closed_restaurant_information_dict = foodsafetykorea_closed_restaurant_information.to_dict()
        return foodsafetykorea_closed_restaurant_information_dict


if __name__ == '__main__':

    foodsafetykorea_closed_restaurant_information_dict = GatherClosedRestaurantData.click_next_page_upload_csv()
