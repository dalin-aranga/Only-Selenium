from selenium import webdriver


with open('buyers.csv','w') as f:
    f.write('Buyers , Price\n')

driver = webdriver.Firefox()
for i in range(1,6):
    url = 'http://econpy.pythonanywhere.com/ex/00'+str(i)+'.html'
    driver.get(url)

    buyers = driver.find_elements_by_xpath('//div[@title="buyer-name"]')
    prices = driver.find_elements_by_xpath('//span[@class ="item-price"]')

    with open('buyers.csv','a') as f:
        for i in range(len(prices)):
            f.write(buyers[i].text+ "," + prices[i].text+'\n')

driver.close()