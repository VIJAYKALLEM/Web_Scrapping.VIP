import time
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

val = input("Please enter the address you want: ")

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.zillow.com/")
time.sleep(2)

while True:
    try:
        if driver.find_element_by_xpath("//input"):
            break
    except Exception:
        time.sleep(5)

input_ele = driver.find_element_by_xpath("//input")
input_ele.send_keys(val)
time.sleep(5)
input_ele.send_keys(Keys.ENTER)
time.sleep(5)

button_ele = driver.find_element_by_xpath("//button[text()='For sale']")
button_ele.click()
time.sleep(2)

input_ele = driver.find_element_by_xpath("//input")
input_ele.send_keys(Keys.CONTROL + "a")
input_ele.send_keys(Keys.DELETE)
input_ele.send_keys(val)
time.sleep(5)
input_ele.send_keys(Keys.ENTER)
time.sleep(5)

address = []
latitude = []
longitude = []
buildingtype = []
floorsize = []
yearbuilt = []
link = []
image = []

pages_ele = driver.find_element_by_xpath("//div[@class='search-pagination']")
pages = pages_ele.text.split(' ')[-1]

next_page_ele = driver.find_element_by_xpath("//a[@title='Next page']")
next_page = next_page_ele.get_attribute('href')
url = next_page[:-4]

urls = [url]
for i in range(2, int(pages)+1):
    urls.append(f"{url}{i}_p/")

for i,url_ in enumerate(urls):
    print(url_)
    print(f'Processing page{i+1}.')
    driver.get(url_)
    time.sleep(2)

    items_ele = driver.find_elements_by_xpath("//div[@id='grid-search-results']/ul/li/script")
    for item_ele in items_ele:
        json_file = json.loads(item_ele.get_attribute('innerHTML'))
        if json_file['@type'] == 'Event':
            pass
        else:
            address.append(json_file['name'])
            latitude.append(json_file['geo']['latitude'])
            longitude.append(json_file['geo']['longitude'])
            buildingtype.append(json_file['@type'])
            floorsize.append(json_file['floorSize']['value'])
            link.append(json_file['url'])

    imgs_ele = driver.find_elements_by_xpath("//div[@id='grid-search-results']/ul/li/article/div/a/img")
    for img_ele in imgs_ele:
        image.append(img_ele.get_attribute('src'))

    df = pd.DataFrame({'Address': address, 'Latitude': latitude, 'Longitude': longitude, 'BuildingType': buildingtype, 'FloorSize': floorsize, 'Link': link, 'Image': image})
    df.to_csv(f"zillow_{val}.csv", index=None)

    # for i in link:       
    #     driver.get(i)
    #     time.sleep(2)
    #     yearbuilt_ele = driver.find_element_by_xpath("//ul[@class='ds-home-fact-list']/li[2]/span[2]")
    #     yearbuilt.append(yearbuilt_ele.text)
    # print(yearbuilt)

    # df = pd.DataFrame({'Address': address, 'Latitude': latitude, 'Longitude': longitude, 'BuildingType': buildingtype, 'FloorSize': floorsize, 'YearBuilt': yearbuilt, 'Link': link, 'Image': image})
    # df.to_csv(f"zillow_{val}.csv", index=None)
