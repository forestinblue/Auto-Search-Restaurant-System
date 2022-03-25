#  python mod1.py
from  selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time as time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time
from tqdm import tqdm
import math
import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_seq_items', 100)
#options = webdriver.ChromeOptions() 
#options.add_argument('--disable-dev-shm-usage') 
#options.add_argument("--disable-features=VizDisplayCompositor");
#options.add_argument("--incognito")
#options.add_argument('--window-size=1920x1080')




class GatherNewRestaurantData:
    #global new_restaurant_information
    #new_restaurant_information = pd.DataFrame(columns = ['name', 'license_number', 'old_address','new_address','zip_code', 'latitude', 'longtitude','index_number'])
    global number_of_new_restaurant
    number_of_new_restaurant = 0
    global crawling_number
    crawling_number = 0
    global capa
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    global options
    options = webdriver.ChromeOptions() 
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument("--disable-features=VizDisplayCompositor");
    options.add_argument("--incognito")
    options.add_argument('--window-size=1920x1080')

    def open_driver_new_restaurant_site():
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        driver.get("http://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoCompany.do?menu_grp=MENU_NEW04&menu_no=2813")
        driver.maximize_window()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="mode1"]/div[1]/div[1]/ul/li[4]/a').click()
        time.sleep(5)
        driver.find_element_by_xpath('//*[@id="srchBtn"]').click()
        time.sleep(10) 
        driver.find_element_by_xpath('//*[@id="sp_list_cnt"]').click() 
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="contents"]/main/section/div[2]/div[2]/div[3]/div/ul/li[5]/a').click()
        #global new_restaurant_information
        #new_restaurant_information = pd.DataFrame(columns = ['name', 'license_number', 'old_address','new_address','zip_code', 'latitude', 'longtitude','index_number'])
        foodsafetykorea_new_information =pd.read_csv('C:/Users/junseok/Downloads/foodsafetykorea_new_information.csv')
        memory_num =foodsafetykorea_new_information.sort_values(by =['index_number'], axis = 0, ascending= False).iloc[0][7]
        global number_of_new_restaurant
        number_of_new_restaurant =  int(driver.find_elements_by_css_selector('#tbl_bsn_list > tbody > tr:nth-child(1) > td:nth-child(1) > span.table_txt')[0].text)  - memory_num
        time.sleep(3)
        print(number_of_new_restaurant)
        return (number_of_new_restaurant)
        
  
    def crawling_new_restaurant_data():
        #global new_restaurant_information
        print("hi")
        new_restaurant_information = GatherNewRestaurantData.clear_restaurant_dataframe()
        time.sleep(10)
        for n in range(1, crawling_number, 1):
            time.sleep(0.1)
            if driver.find_elements_by_css_selector(f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(4) > span.table_txt')[0].text == '위탁급식영업' or driver.find_elements_by_css_selector(f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(4) > span.table_txt')[0].text =='집단급식소':
                pass
            else:
                n_index_number = driver.find_elements_by_css_selector(f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(1) > span.table_txt')[0].text   
                n_license_number = driver.find_elements_by_css_selector(f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(2) > span.table_txt')[0].text
                n_name = driver.find_elements_by_css_selector(f'#tbl_bsn_list > tbody > tr:nth-child({n}) > td:nth-child(3) > span.table_txt')[0].text
                n_new_address = driver.find_elements_by_css_selector(f'#tbl_bsn_list > tbody > tr:nth-child({n}n) > td:nth-child(6) > span.table_txt')[0].text
                n_old_address = ''
                n_zip_code = '' 
                n_longtitude = ''
                n_latitude = ''
                new_restaurant_information = new_restaurant_information.append({'name':n_name,  'new_address':n_new_address,'old_address':n_old_address,  'zip_code': n_zip_code ,'license_number':n_license_number,'index_number':n_index_number, 'latitude':n_latitude, 'longtitude':n_longtitude }, ignore_index=True) #, 'phonenumber':phonenumber, 'menu': menu,
                #new_restaurant_information.drop_duplicates(inplace = True)
                print(n_index_number)
                print(n_license_number)
                print(n_name)
                print(n_old_address)
            return_dataframe  = new_restaurant_information
        return return_dataframe
    
    def clear_restaurant_dataframe():
        new_dataframe = pd.DataFrame(columns = ['name', 'license_number', 'old_address','new_address','zip_code', 'latitude', 'longtitude','index_number'])
        return(new_dataframe)
    
    def click_next_page_upload_csv():
        
        number_of_new_restaurant = GatherNewRestaurantData.open_driver_new_restaurant_site()
        print(number_of_new_restaurant)
        count  = 0
        page_number = number_of_new_restaurant / 50
        page_number = int(math.ceil(page_number))
        print(f'we will crawling {page_number} of pages')

        for page_count in tqdm(range(page_number)) :
            print('count= ' , count)
            count += 1
            print(page_number)
            print("aha")
            while True:
                print(">!")
                if number_of_new_restaurant >= 1:
                    
                    if number_of_new_restaurant >= 50:
                        number_of_new_restaurant -= 50
                        global crawling_number
                        crawling_number = 50
                    else:
                        crawling_number = number_of_new_restaurant
                        number_of_new_restaurant = 0
                print("ahaha")
                crawling_dataframe = GatherNewRestaurantData.crawling_new_restaurant_data()
                driver.find_element_by_css_selector('#contents > main > section > div.board-footer > div > ul > li:nth-child(7) > a').click()
                time.sleep(2)
                foodsafetykorea_new_information =pd.read_csv('C:/Users/junseok/Downloads/foodsafetykorea_new_information.csv')
                foodsafetykorea_new_information = foodsafetykorea_new_information.append(crawling_dataframe)
                foodsafetykorea_new_information.to_csv('C:/Users/junseok/Downloads/foodsafetykorea_new_information.csv', index = None)
                print('update csv')
                break


    def open_driver_lat_lon_site(): 
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install() , desired_capabilities=capa)
        wait = WebDriverWait(driver, 3)
        driver.get("https://address.dawul.co.kr/index.php")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#addrProRs')))
        time.sleep(1)
        driver.execute_script("window.stop();")
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1]) # 팝업창을 선택
        time.sleep(0.5)
        print('1')
        driver.close() # 팝업창 삭제
        time.sleep(0.5)
        print('2')
        driver.switch_to.window(driver.window_handles[0]) # main창 선택
        time.sleep(0.5)
        print('3')


    def crawling_lat_lon_data():
        GatherNewRestaurantData.open_driver_lat_lon_site()
        print('4')
        time.sleep(3)
        foodsafetykorea_new_information =pd.read_csv('C:/Users/junseok/Downloads/foodsafetykorea_new_information.csv')
        upload_dataframe = foodsafetykorea_new_information.loc[foodsafetykorea_new_information.old_address.isnull()]
        upload_dataframe.reset_index(drop=True, inplace=True)
        newborn_restaurant_address = list(upload_dataframe['new_address']) #new_address로 수정 , test로 old_address
        search_box = driver.find_element(By.NAME, "juso")
        for i in range(len(upload_dataframe)):
            while True:
                search_box.clear()
                search_box.send_keys(newborn_restaurant_address[i])
                search_box.send_keys(Keys.RETURN) 
                time.sleep(1.5)
                try:
                    upload_dataframe['old_address'][i] = driver.find_elements_by_css_selector('#insert_data_3 ')[0].text  #지번 주소
                except Exception as e:
                    print(e)
                    upload_dataframe['old_address'][i]  = ''
                try:
                    upload_dataframe['zip_code'][i] = driver.find_elements_by_css_selector('#insert_data_4')[0].text
                except Exception as e:
                    print(e)
                    upload_dataframe['zip_code'][i] =''
                n_lat_lon = driver.find_elements_by_css_selector('#insert_data_5')[0].text  
                n_lon = n_lat_lon.split(',')[0]
                n_lat = n_lat_lon.split(',')[1]
                n_lon  = n_lon[3:]
                n_lat =   n_lat[4:]
                print()
                
                

                try:
                    upload_dataframe['latitude'][i] = n_lat
                except Exception as e:
                    print(e)
                    upload_dataframe['latitude'][i] = ''
                try :
                    upload_dataframe['longtitude'][i] = n_lon
                except Exception as e:
                    print(e)
                    upload_dataframe['longtitude'][i] =  ''
                    
                print(upload_dataframe['old_address'][i])    
                print(upload_dataframe['zip_code'][i])
                print(upload_dataframe['latitude'][i])
                print(upload_dataframe['longtitude'][i])
                    
                    

                n_lat_lon = ''
                n_lat = ''
                n_lon = ''
                break 
                        
        upload_dataframe.to_csv('C:/Users/junseok/Downloads/foodsafetykorea_new_information.csv', index = None)
        
        
        
