import json
import time

from selenium import webdriver


def dump_json(data, path):
    """
    Save JSON object to file.
    :param data: dict
    :param path: str
    """
    with open(path, 'w+') as f:
        json.dump(data, f)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome('./chromedriver', options=chrome_options)

driver.get('https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=shipname')

time.sleep(2)

driver.find_elements_by_css_selector("button.qc-cmp-button")[1].click()

data = {'names': []}

while True:
    elements = driver.find_elements_by_css_selector('a.ag-cell-content-link')
    names = [i.text.lower() for i in elements if i != '']

    print(names)

    data['names'] += names

    try:
        driver.find_elements_by_css_selector("button[title='Next page']")[0].click()
    except:
        break

dump_json(data, './cache/vessel_data.json')
