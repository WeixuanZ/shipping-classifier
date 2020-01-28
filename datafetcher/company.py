import json
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def dump_json(data, path):
    """
    Save JSON object to file.
    :param data:
    :param filename:
    :return:
    """
    with open(path, 'w+') as f:
        data = json.dump(data, f)
    return data


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome('./chromedriver', options=chrome_options)

# urls = ['https://opencorporates.com/companies?utf8=✓&q={}&commit=Go&jurisdiction_code=&controller=searches&action=search_companies&order='.format(chr(i)) for i in range(ord('a'),ord('z')+1)]

urls = ['hhttps://opencorporates.com/companies/gb?action=search_companies&commit=Go&controller=searches&order=score&q=&utf8=✓', 'https://opencorporates.com/companies?utf8=✓&q=&commit=Go&jurisdiction_code=&country_code=us&controller=searches&action=search_companies&order=score', 'https://opencorporates.com/companies/ca?action=search_companies&commit=Go&controller=searches&order=score&q=&utf8=✓', 'https://opencorporates.com/companies/sg?action=search_companies&commit=Go&controller=searches&order=score&q=&utf8=✓', 'https://opencorporates.com/companies/fr?action=search_companies&commit=Go&controller=searches&order=score&q=&utf8=✓', 'https://opencorporates.com/companies/dk?action=search_companies&commit=Go&controller=searches&order=score&q=&utf8=✓', 'https://opencorporates.com/companies/fi?action=search_companies&commit=Go&controller=searches&order=score&q=&utf8=✓', 'https://opencorporates.com/companies/hk?action=search_companies&commit=Go&controller=searches&order=score&q=&utf8=✓']

time.sleep(2)

data = {'names': []}

for url in urls:

    driver.get(url)

    while True:
        
        elements = driver.find_elements_by_css_selector("a.company_search_result")
        names = [i.text.lower() for i in elements]

        if len(names) == 0:
            break

        print(names)

        data['names'] += names

        time.sleep(5)

        try:
            driver.find_elements_by_css_selector("a[rel='next nofollow']")[0].click()
        except:
            break

dump_json(data, './cache/company_data.json')
