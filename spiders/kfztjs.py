import scrapy
import json


class Dalin(scrapy.Spider):
    name = 'kfztjs'
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            'First Name',
            'Second Name',
            'Last Name'
        ]
    };

    def start_requests(self):
        start = 'https://www.kfzteile24.de/'
        yield scrapy.Request(url=start,callback=self.parse)

    def parse(self, response):
        val_num = []
        namelist1 =[]
        try:
            dd = response.xpath('//select[@id="typeSelectionField_1"]/optgroup/option')
            for d in dd:
                a = d.xpath('.//@value').extract_first()
                name1 = d.xpath('.//text()').extract_first()
                namelist1.append(name1)
                val_num.append(a)

        except:
            pass
        for j in range(0, len(val_num)):
            part = 'https://www.kfzteile24.de/index.cgi?rm=headerChooseType&hernr='
            url = part + val_num[j]
            yield scrapy.Request(url=url, callback=self.inside,meta={'namelist1': namelist1[j]})

    def inside(self, response):
        namelist1 = response.meta['namelist1']
        p = json.loads(response.body.decode('utf-8'))
        model_val = []
        namelist2 = []
        try:
            i=0
            while True:
                a = p['models'][i]['value']
                name = p['models'][i]['name']
                namelist2.append(name)
                model_val.append(a)
                i=i+1
        except:
            pass
        for j in range(0,len(model_val)):
            url= response.url+'&kmodnr='+model_val[j]
            name2 = response.xpath('//select[@id="typeSelectionField_2"]/option/text()').extract_first()
            namelist2.append(name2)
            yield scrapy.Request(url=url,callback=self.parseOut, meta={'namelist1':namelist1, 'namelist2':namelist2[j]})

    def parseOut(self,response):
        p = json.loads(response.body.decode('utf-8'))
        try:
            i=0
            while True:
                namelist1 = response.meta['namelist1']
                namelist2 = response.meta['namelist2']
                name3 = p['models'][i]['name']

                yield {
                    'First Name': namelist1,
                    'Second Name': namelist2,
                    'Last Name': name3
                }
                i=i+1

        except:
            pass


