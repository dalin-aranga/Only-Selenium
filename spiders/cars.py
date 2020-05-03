import scrapy


class Tutu(scrapy.Spider):
    name = 'cars'
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            'Brand',
            'Condition',
            'Price',
            'Mileage',
            'Transmition',
            'VIN',
            'Image Link'
        ]

    };
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.129 Chrome/81.0.4044.129 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    def start_requests(self):
        for i in range(1,22):
            url = 'https://www.porschevancouver.ca/inventory?page='+str(i)
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        a = response.xpath('//div[@class ="vehicle-listing used"]')
        for aa in a:
            image_url = response.xpath('.//div[@class="vehicle-listing-photo"]/img/@src').extract_first()
            brand = aa.xpath('.//div[@class ="vehicle-listing-ymm"]/a/text()').extract_first().strip()
            link = 'https://www.porschevancouver.ca'+ aa.xpath('.//div[@class ="vehicle-listing-ymm"]/a/@href').extract_first()
            yield scrapy.Request(url=link, callback=self.details, headers=self.headers, meta={'brand': brand,'image':image_url})

    def details(self, response):
        image_url = response.meta['image']
        brand = response.meta['brand']
        price = response.xpath('//dd/strong[@id ="vehicle-detail-price"]/text()').extract_first()
        condition = response.xpath('//dd[2]/text()').extract_first()
        mileage = response.xpath('//dd[3]/text()').extract_first().replace('\xa0','')
        transmision = response.xpath('//dd[4]/text()').extract_first()
        vin = response.xpath('//dd[5]/text()').extract_first()
        yield {
            'Brand': brand,
            'Condition': condition,
            'Price': price,
            'Mileage': mileage,
            'Transmition': transmision,
            'VIN': vin,
            'Image Link': image_url
        }






