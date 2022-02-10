import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json


chromedriver_path = '/usr/local/bin/chromedriver'
brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_argument("--headless")
browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)

def get_neighborhood_urls():
    browser.get("https://sundlaugar.is/sundlaugar/")
    urls = []
    neighborhoods = browser.find_elements_by_css_selector('#wrapper > div.region-buttons-area > div > ul > a')
    for neighborhood in neighborhoods:
        urls.append(neighborhood.get_attribute("href") + '\n')

    with open('neighborhood_urls.txt', 'w') as f:
        f.writelines(urls)

def get_pool_data(urls):
    data = {}
    for url in urls:
        nh = url.split('landshlutar/')[1]
        browser.get(url)
        pools = browser.find_elements_by_css_selector('#wrapper > div.latest-posts > div.swp-listing > ul > li > a')
        data[nh] = {
            'url': url,
            'pool_urls': [p.get_attribute('href') for p in pools]
        }
        with open('neighborhood_pools.json', 'w') as f:
            json.dump(data,f)

def get_all_pool_data():
    pools = []
    with open('neighborhood_pools.json') as json_file:
        data = json.load(json_file)


        for index, nh in enumerate(data):
            for pool_url in data[nh]['pool_urls']:
                browser.get(pool_url)
                try:
                    pool_name = browser.find_elements_by_css_selector('div.swp-headlines > h2')[0].get_attribute('innerText')
                except:
                    pool_name = ''
                try:
                    pool_address = browser.find_elements_by_css_selector('div.swp-headlines > a > h4')[0].get_attribute('innerText')
                except:
                    pool_address = ''

                browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                try:
                    pool_coordinates = browser.find_element_by_css_selector('div.acf-map > iframe').get_attribute('src').split('q=')[1].replace('%20-','')
                except:
                    pool_coordinates = ''
                print({pool_name,pool_address,pool_coordinates})
                pools.append({
                    'name': pool_name,
                    'address': pool_address,
                    'coordinates': pool_coordinates,
                    'neighborhood': nh
                })
                # browser.close()
        
    with open('pools.json', 'w') as f:
        json.dump(pools,f)

get_all_pool_data()



# get_neighborhood_urls()

# with open('neighborhood_urls.txt', 'r') as f:
#     urls = [u for u in f.readlines()]
# get_pool_data(urls)