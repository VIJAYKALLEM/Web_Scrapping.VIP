import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

val = input("Please enter the address you want: ")

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.trulia.com/")
time.sleep(1)

while True:
    try:
        if driver.find_element_by_xpath("//input[@data-testid='location-search-input']"):
            break
    except Exception:
        time.sleep(5)

input_ele = driver.find_element_by_xpath("//input[@data-testid='location-search-input']")
input_ele.send_keys(Keys.CONTROL + "a")
input_ele.send_keys(Keys.DELETE)
input_ele.send_keys(val)
input_ele.send_keys(Keys.ENTER)
time.sleep(5)

cur_url = driver.current_url

try:
    pages_ele = driver.find_elements_by_xpath("//div[@data-testid='search-results-pagination']/ul/li/a")[-2]
    pages = pages_ele.text

    urls = [cur_url]

    for i in range(2,int(pages)+1):
        urls.append(f"{cur_url}/{i}_p/")

except Exception:
    urls = [cur_url]

address = []
floorsize = []

for i,url in enumerate(urls):
    print(f'Processing page{i+1}.')
    driver.get(url)
    time.sleep(2)

    streets_ele = driver.find_elements_by_xpath("//div[@data-testid='property-street']")
    regions_ele = driver.find_elements_by_xpath("//div[@data-testid='property-region']")

    for idx,street_ele in enumerate(streets_ele):
        address.append(street_ele.text + ' ' + regions_ele[idx].text)

    links = []

    links_ele = driver.find_elements_by_xpath("//div[@data-testid='home-card-sale']/a")
    for link_ele in links_ele:
        links.append(link_ele.get_attribute('href'))

    for link in links:
        driver.get(link)
        time.sleep(2)

        try:
            size_ele = driver.find_element_by_xpath("//li[@data-testid='floor']")
            floorsize.append(size_ele.text)
        except Exception:
            floorsize.append('N/A')

    df = pd.DataFrame({'Address': address, 'FloorSize': floorsize})
    df.to_csv(f"trulia_{val}.csv", index=None)
  