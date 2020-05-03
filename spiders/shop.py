# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class Shop(scrapy.Spider):
    name = 'shop'

    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [

            'Name',
            'Nobel',
            'Manufacture',
            'MPN',
            'Country',
            'Abilityone',
            'Contracts',
            'Earth',
            'Grainger',
            'GSA',
            'SDS',
            'NSN',
            'Quntity',
            'PSN',
            'UOM',
            'UPC',
            'Weight',
            'URL',
            'Description'

        ]
    };

    def start_requests(self):
        data = pd.read_csv("/train/sho_p.csv", usecols=['linku'])
        links = data['linku']
        for url in links:
            yield scrapy.Request(url=url, callback=self.parse, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36'})

    def parse(self, response):
        url = response.url
        name = response.xpath('//span[@class= "h1"]/text()').extract_first()
        nobel = response.xpath('//div[@class ="quick-overview"]/ul/li/span/text()')[0].extract()
        manufature = response.xpath('//div[@class ="quick-overview"]/ul/li/span/text()')[1].extract()
        mpn = response.xpath('//div[@class ="quick-overview"]/ul/li/span/text()')[2].extract()
        contry = response.xpath('//div[@class ="quick-overview"]/ul/li/span/text()')[3].extract()
        description =  response.xpath('//div[@class ="std"]/text()').extract_first().strip()
        abilityone = response.xpath('//div[@class ="product-specs-container"]/span/text()')[0].extract()
        contracts = response.xpath('//div[@class ="product-specs-container"]/span/text()')[1].extract()
        earth = response.xpath('//div[@class ="product-specs-container"]/span/text()')[3].extract()
        grainger = response.xpath('//div[@class ="product-specs-container"]/span/text()')[4].extract()
        gsa = response.xpath('//div[@class ="product-specs-container"]/span/text()')[5].extract()
        sds = response.xpath('//div[@class ="product-specs-container"]/span/text()')[8].extract()
        nsn = response.xpath('//div[@class ="product-specs-container"]/span/text()')[9].extract()
        quntity = response.xpath('//div[@class ="product-specs-container"]/span/text()')[10].extract()
        psn = response.xpath('//div[@class ="product-specs-container"]/span/text()')[11].extract()
        uom = response.xpath('//div[@class ="product-specs-container"]/span/text()')[12].extract()
        upc =response.xpath('//div[@class ="product-specs-container"]/span/text()')[13].extract()
        weiight = response.xpath('//div[@class ="product-specs-container"]/span/text()')[14].extract()

        yield {
            'Name': name,
            'Nobel': nobel,
            'Manufacture': manufature,
            'MPN': mpn,
            'Country': contry,
            'Abilityone': abilityone,
            'Contracts': contracts,
            'Earth': earth,
            'Grainger': grainger,
            'GSA': gsa,
            'SDS': sds,
            'NSN':nsn,
            'Quntity': quntity,
            'PSN': psn,
            'UOM': uom,
            'UPC': upc,
            'Weight': weiight,
            'URL': url,
            'Description': description

        }

