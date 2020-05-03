from time import sleep

import scrapy
import selenium

from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class HomesSpider(Spider):
    name = 'homes'
    start_urls = ('http://books.toscrape.com/',)

    def parse(self, response):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36'}
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--incognito")
        options.add_argument("--disable-extensions")
        options.add_argument(" --disable-gpu")
        options.add_argument(" --disable-infobars")
        options.add_argument(" -–disable-web-security")
        options.add_argument("--no-sandbox")
        caps = options.to_capabilities()

        self.driver = webdriver.Chrome('/bin/chromedriver',desired_capabilities=caps)

        self.driver.get('https://www.airbnb.ae/')
        search_city = self.driver.find_element_by_xpath('//*[@type="text"]').send_keys('Dubai\ue007')
        sleep(0.8)
        search_button = self.driver.find_element_by_xpath('//*[@type="submit"]')
        search_button.click()
        sleep(10.7)
        homes_button = self.driver.find_element_by_xpath('//*[@data-veloute="explore-nav-card:/homes"]')
        homes_button.click()
        sleep(4.2)
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(7)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            sleep(1.2)
        scrapy_selector = Selector(text=self.driver.page_source)
        homes_selector = scrapy_selector.xpath(
            '//*[@itemtype="http://schema.org/ListItem"]')  # name of an item can be changed by Airbnb
        self.logger.info('Theres a total of ' + str(len(homes_selector)) + ' links.')
        profile_urls_distinct = []
        try:
            s = 0
            for home_selector in homes_selector:
                url = home_selector.xpath('//*[@itemprop = "url"]/@content').extract()[s]
                if '/rooms/plus/' not in url:
                    profile_url = 'https://' + url.replace('adults=0&children=0&infants=0&guests=0',
                                                           'adults=1&guests=1&toddlers=0')
                    profile_urls_distinct.append(profile_url)
                    s = s + 1
                else:
                    s = s + 1
        except:
            self.logger.info('Reached last iteration #' + str(s))

        q = 1
        for profile_url in profile_urls_distinct:
            self.logger.info('Home #' + str(q))
            self.driver.get(profile_url)
            q = q + 1
            sleep(10)
            link_to_home = profile_url

            profile_scrapy_selector = Selector(text=self.driver.page_source)
            property_type = profile_scrapy_selector.xpath(
                '//*[@class="_1kzvqab3"]/div/div/div[3]/div/div/div/div[2]/div/text()').extract_first()
            summary = profile_scrapy_selector.xpath(
                '//*[@class="_1kzvqab3"]/div/div/div[3]/div/div/div/div[2]/div[2]/div/div/text()').extract()
            property_name = profile_scrapy_selector.xpath('//*[@itemprop="name"]//h1/span/text()').extract()
            price_night = profile_scrapy_selector.xpath('//*[@class ="_doc79r"]/text()').extract_first()
            rating_overall = profile_scrapy_selector.xpath('//*[@itemprop="ratingValue"]/@content').extract_first()
            rating_split = {}
            rating_categories = profile_scrapy_selector.xpath('//*[@class="_iq8x9is"]/span/text()').extract()
            rating_stars = profile_scrapy_selector.xpath('//*[@class="_iq8x9is"]/div/span//@aria-label').extract()
            i = 0
            for i in range(len(rating_categories)):
                rating_split[rating_categories[i]] = rating_stars[i]
                i = i + 1
            home_neighborhood_short = profile_scrapy_selector.xpath(
                '//*[@class="_6z3til"]//*[@class="_czm8crp"]/span/text()').extract()
            reviews_dict = {}
            reviews_list = []
            sleep(2)
            try:
                sleep(4)
                reviews_button = self.driver.find_element_by_xpath('//*[@class="_ff6jfq"]')
                reviews_button.click()
                k = 0
                profile_scrapy_selector_1 = Selector(text=self.driver.page_source)
                #				reviewers = profile_scrapy_selector_1.xpath('//*[@id = "reviews"]//section/div[2]//*[@class="_hgs47m"]/div[2]/div[1]/div/div/text()').extract()
                #				review_dates = profile_scrapy_selector_1.xpath('//*[@id = "reviews"]//section/div[2]//*[@class="_hgs47m"]/div[2]/div[1]/div/span/text()').extract()
                #				reviews = profile_scrapy_selector_1.xpath('//*[@id = "reviews"]//section/div[2]//*[@dir="ltr"]/text()').extract()
                reviews = profile_scrapy_selector_1.xpath(
                    '//*[@id = "reviews"]//section/div[2]//*[@style="margin-top: 16px;"]/div//*[@dir="ltr"]/text()').extract()
                reviews_list.append(reviews)
                #				for k in range(len(reviewers)):
                #					reviewer_date = reviewers[k] + ' >> ' + review_dates[k]
                #					review = reviews[k]
                #					reviews_dict[reviewer_date] = review
                #					k = k+1
                while True:
                    #					j = 0
                    sleep(2.15)
                    try:
                        next_button = self.driver.find_element_by_xpath('//*[@class="_1rltvky"]//*[@aria-label="Next"]')
                        sleep(1)
                        next_button.click()
                        sleep(2.1)
                        reviews_scrapy_selector = Selector(text=self.driver.page_source)
                        #						reviewers = reviews_scrapy_selector.xpath('//*[@id = "reviews"]//section/div[2]//*[@class="_hgs47m"]/div[2]/div[1]/div/div/text()').extract()
                        #						review_dates = reviews_scrapy_selector.xpath('//*[@id = "reviews"]//section/div[2]//*[@class="_hgs47m"]/div[2]/div[1]/div/span/text()').extract()
                        #						reviews = reviews_scrapy_selector.xpath('//*[@id = "reviews"]//section/div[2]//*[@dir="ltr"]/text()').extract()
                        reviews_1 = reviews_scrapy_selector.xpath(
                            '//*[@id = "reviews"]//section/div[2]//*[@style="margin-top: 16px;"]/div//*[@dir="ltr"]/text()').extract()
                        reviews_list.append(reviews_1)
                    #						for j in range(len(reviewers)):
                    #							reviewer_date = reviewers[j] + ' >> ' + review_dates[j]
                    #							review = reviews[j]
                    #							reviews_dict[reviewer_date] = review
                    #							j = j+1
                    #							sleep(1.1)
                    except:
                        self.logger.info('Failed to navigate the Next page in Reviews.')
                        yield {
                            'link_to_home': link_to_home,
                            'property_type': property_type,
                            'property_name': property_name,
                            'price_night': price_night,
                            'rating_overall': rating_overall,
                            'rating_split': rating_split,
                            'summary': summary,
                            'home_neighborhood_short': home_neighborhood_short,
                            #						'reviews_dict' : reviews_dict
                            'reviews': reviews_list
                        }
                        break
            except NoSuchElementException:
                self.logger.info('No Reviews section to navigate to.')
                yield {
                    'link_to_home': link_to_home,
                    'property_type': property_type,
                    'property_name': property_name,
                    'price_night': price_night,
                    'rating_overall': rating_overall,
                    'rating_split': rating_split,
                    'summary': summary,
                    'home_neighborhood_short': home_neighborhood_short,
                    'reviews': reviews_list
                    #				'reviews_dict' : reviews_dict
                }
        self.driver.close()