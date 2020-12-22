import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

val = input("Please enter the address you want: ")

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.realtor.com/?cid=sem_google_desktop_far_exact_net_new&medium=tsa&ds_kid=43700059183991574&s_kwcid=AL!5154!3!442356331358!e!!g!!reator&ef_id=Cj0KCQiA2uH-BRCCARIsAEeef3kIw4skmO3eJZhw_Zo7S5DqSt_4QApzcRvplRWijcUdbLONo-XWZqsaAk3mEALw_wcB:G:s&gclid=Cj0KCQiA2uH-BRCCARIsAEeef3kIw4skmO3eJZhw_Zo7S5DqSt_4QApzcRvplRWijcUdbLONo-XWZqsaAk3mEALw_wcB&gclsrc=aw.ds")
time.sleep(1)

input_ele = driver.find_element_by_xpath("//input[@data-testid='input-element']")
input_ele.send_keys(val)
input_ele.send_keys(Keys.ENTER)
time.sleep(5)

cur_url = driver.current_url
pages_ele = driver.find_elements_by_xpath("//div[@data-testid='pagination']/a")[-2]
pages = pages_ele.text.split(' ')[-1]

urls = [cur_url]

for i in range(2,int(pages)+1):
    urls.append(f"{cur_url}/pg-{i}/")

address = []
size = []
yearbuilt = []
lotsize = []
image = []

for url in urls:
    driver.get(url)
    time.sleep(2)

    links = []

    while True:
        if driver.find_elements_by_xpath("//ul[@data-testid='property-list-container']/li/div/div[2]/div/a"):
            break
        else:
            time.sleep(5)

    items = driver.find_elements_by_xpath("//ul[@data-testid='property-list-container']/li/div/div[2]/div/a")

    for item in items:
        links.append(item.get_attribute('href'))
        links = list(set(links))

    for link in links:
        driver.get(link)
        time.sleep(2)

        address_ele = driver.find_element_by_xpath("//div[@data-testid='address-section']")
        address.append(address_ele.text)

        pic_ele = driver.find_element_by_xpath("//img[@itemprop='image']")
        image.append(pic_ele.get_attribute('data-src'))

        try:
            size_ele = driver.find_element_by_xpath("//li[@data-label='pc-meta-sqft']")
            size.append(size_ele.text)
        except Exception:
            size.append('N/A')

        try:
            lotsize_ele = driver.find_element_by_xpath("//li[@data-label='pc-meta-sqftlot']")
            lotsize.append(lotsize_ele.text)
        except Exception:
            lotsize.append('N/A')

        try:
            ks_ele = driver.find_elements_by_xpath("//div[@data-testid='listing-summary-indicators-cmp']/ul/li/div/span[1]")
            vs_ele = driver.find_elements_by_xpath("//div[@data-testid='listing-summary-indicators-cmp']/ul/li/div/span[2]")

            ks = [k_ele.text for k_ele in ks_ele]

            if 'Year Built' not in ks:
                yearbuilt.append('N/A')
            else:
                for k in ks:
                    if k == 'Year Built':
                        yearbuilt.append(vs_ele[ks.index(k)].text)
        except Exception:
            yearbuilt.append('N/A')

        df = pd.DataFrame({'Address': address, 'Size': size, 'LotSize': lotsize, 'YearBuilt': yearbuilt, 'Image': image})
        df.to_csv(f"realtor_{val}.csv", index=None)
