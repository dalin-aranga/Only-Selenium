# -*- coding: utf-8 -*-
import scrapy


class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': [
            'Catagory',
            'Name',
            'Seasion',
            'Genrec',
            'Meta Score',
            'User Score',
            'Network',
            'Crities Review',
            'User Review',
            'Criteas',
            'Summary',
            'URL'

        ]
    };

    def start_requests(self):
        urls = [
            'https://www.metacritic.com/browse/tv/genre/name/arts?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/business?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/educational?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/educational?view=condensed&page=1'
            'https://www.metacritic.com/browse/tv/genre/name/eventsspecials?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/foodcooking?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/kids?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/kids?view=condensed&page=1'
            'https://www.metacritic.com/browse/tv/genre/name/news?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/science?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/science?view=condensed&page=1'
            'https://www.metacritic.com/browse/tv/genre/name/soap?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/sports?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/sports?view=condensed&page=1'
            'https://www.metacritic.com/browse/tv/genre/name/talkinterview?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/talkinterview?view=condensed&page=1'
            'https://www.metacritic.com/browse/tv/genre/name/talkinterview?view=condensed&page=2'
            'https://www.metacritic.com/browse/tv/genre/name/techgaming?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/travel?view=condensed',
            'https://www.metacritic.com/browse/tv/genre/name/variety-shows?view=condensed'
        ]

        for i in range(1,19):
            link = 'https://www.metacritic.com/browse/tv/genre/name/actionadventure?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,41):
            link = 'https://www.metacritic.com/browse/tv/genre/name/comedy?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,10):
            link = 'https://www.metacritic.com/browse/tv/genre/name/documentary?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,4):
            link = 'https://www.metacritic.com/browse/tv/genre/name/animation?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,68):
            link = 'https://www.metacritic.com/browse/tv/genre/name/drama?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,8):
            link = 'https://www.metacritic.com/browse/tv/genre/name/fantasy?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,6):
            link = 'https://www.metacritic.com/browse/tv/genre/name/gameshow?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,3):
            link = 'https://www.metacritic.com/browse/tv/genre/name/healthlifestyle?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,):
            link = 'https://www.metacritic.com/browse/tv/genre/name/horror?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,12):
            link = 'https://www.metacritic.com/browse/tv/genre/name/moviemini-series?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,5):
            link = 'https://www.metacritic.com/browse/tv/genre/name/music?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,5):
            link = 'https://www.metacritic.com/browse/tv/genre/name/newsdocumentary?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,11):
            link = 'https://www.metacritic.com/browse/tv/genre/name/reality?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,10):
            link = 'https://www.metacritic.com/browse/tv/genre/name/sciencefiction?view=condensed&page='+str(i)
            urls.append(link)
        for i in range(1,17):
            link = 'https://www.metacritic.com/browse/tv/genre/name/suspense?view=condensed&page='+str(i)
            urls.append(link)
        for url in urls:

            yield scrapy.Request(url=url, callback=self.parse,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36'})

    def parse(self, response):
        catagory = response.xpath('//ul[@class ="genre_nav"]/li/span/text()').extract_first()
        catogry = response.xpath('//div[@class="basic_stat product_title"]/a')
        for cat in catogry:
            a_tag = cat.xpath('.//@href').extract_first()
            link = 'https://www.metacritic.com' + a_tag
            yield scrapy.Request(url=link, callback=self.details,meta={'catagory': catagory}, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36'})

    def details(self,response):
        catagory = response.meta['catagory']
        url = response.url
        name = response.xpath('//div[@class= "product_page_title oswald"]/h1/a/text()').extract_first()
        seasion = response.xpath('//div[@class= "product_page_title oswald"]/h1/text()').extract_first()
        summary = response.xpath('//div[@class="summary_deck details_section"]/span/span/text()').extract_first()
        genrec = response.xpath('////div[@class="genres"]/span/span/text()').extract()
        network = response.xpath('//table[@class="cert_rating_wrapper"]//tr/td/span/a/text()').extract_first()
        if response.xpath('//div[@class="metascore_w larger tvshow mixed"]/text()').extract_first():
            metascore = response.xpath('//div[@class="metascore_w larger tvshow mixed"]/text()').extract_first()
        else:
            metascore = response.xpath('//div[@class="metascore_w larger tvshow positive"]/text()').extract_first()
        userscore = response.xpath('//div[@class="metascore_w user larger tvshow positive"]/text()').extract_first()
        critics = response.xpath('//div[@class="score_wrap"]/div[@class="metascore_w header_size tvshow positive indiv"]/text()').extract()
        mp = int(response.xpath('//div[@class="count fr"]/text()')[0].extract().replace(',',''))
        mm = int(response.xpath('//div[@class="count fr"]/text()')[1].extract().replace(',',''))
        mn = int(response.xpath('//div[@class="count fr"]/text()')[2].extract().replace(',',''))
        up = int(response.xpath('//div[@class="count fr"]/text()')[3].extract().replace(',',''))
        um = int(response.xpath('//div[@class="count fr"]/text()')[4].extract().replace(',',''))
        un = int(response.xpath('//div[@class="count fr"]/text()')[5].extract().replace(',',''))
        metareview = mp+mm+mn
        userreview = um+up+un



        yield {
            'Catagory': catagory,
            'Name': name,
            'Seasion': seasion,
            'Genrec': genrec,
            'Meta Score': metascore,
            'User Score': userscore,
            'Network': network,
            'Crities Review': metareview,
            'User Review': userreview,
            'Criteas': critics,
            'Summary': summary,
            'URL': url
        }













