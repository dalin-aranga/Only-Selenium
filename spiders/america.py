import json
import time
from selenium import webdriver

cod =[]
outcode = []
with open('house.csv','w') as f:
    f.write('House name\n')

with open('/home/dalin/PycharmProjects/scrapy/train/train/spiders/postcodes.json') as j:
    data = json.load(j)
    for i in data:
        try:
            cod.append(i['postcode'])
            outcode.append(i['locationId'][8:])
        except TypeError:
            pass
driver = webdriver.Firefox()

j = 0

while True:
    try:
        url = 'https://www.rightmove.co.uk/house-prices/detail.html?country=england&locationIdentifier=OUTCODE%5E'+ outcode[j] +'&searchLocation=' + cod[j]
        driver.get(url)
        driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
        time.sleep(1.5)
        name = driver.find_elements_by_xpath('//a[@class = "title clickable"]')
        noname = driver.find_elements_by_xpath('//div[@class="propertyCard-content"]/div[@class = "title"]')
        with open('house.csv','a') as f:
            for i in name:
                f.write(i.text+'\n')
            for k in noname:
                f.write(k.text+'\n')
        j = j+1
    except IndexError:
        break







