# -*- coding: utf-8 -*-
# -*- scrapy : tripadvisor chaing mai Restaurant -*-
#  -*- start URL :  https://www.tripadvisor.com/RestaurantSearch-g293917-Chiang_Mai.html" -*-
# -*- note : if you want to save data to database, you need to change pipelines.py and setting.py-*-
# -*- time :2019 7 20-*-


import scrapy
import re
from scrapy.http import Request
from tripadvisor.items import TripadvisorItem


class TripSpider(scrapy.Spider):
    name = "trip"
    allowed_domains = ["https://www.tripadvisor.com"]

    def start_requests(self):
        #  collet index page to start_URL
        for i in range(1,72):
             start_urls = "https://www.tripadvisor.com/RestaurantSearch-g293917-oa'+str(30*i)+'-Chiang_Mai.html"
             # print(start_urls)  print URL and check it
             # send request to parse function
             yield Request(start_urls,self.parse, dont_filter=True)

    def parse(self, response):
        # analyse index page, find all detail page url
        for i in range(1,31):
            restauranturl = response.xpath("//*[@data-index='"+str(i)+"']//*[@class='title']/a/@href").extract() # extract detail page URL

            restauranturls = "https://www.tripadvisor.com" + restauranturl[0]

            # print(restauranturls) print URL and check it
            #
            yield Request(restauranturls,callback=self.detail_page,dont_filter=True)

    def detail_page(self, response):
        # collect  how many reviwe URLs have in detail page
        pagetNum = response.xpath("//*[@class='unified ui_pagination ']//a/@data-page-number")[-1].extract() # maximal number of review page
        pageurl = response.xpath("//*[@class='unified ui_pagination ']//a/@href")[-1].extract()


        # analyse review page URL regulation
        list_i=pageurl.split('Reviews-or',1)
        findstrurl = '-'
        a = [m.start() for m in re.finditer(findstrurl, list_i[-1])]
        last=list_i[-1]
        foreurl = list_i[0]
        foreurls =foreurl
        lasturl =last[a[0]:]

        max_num = int(pagetNum)
        # collect all review URLs
        for i in range(max_num):
            reviewurl= 'https://www.tripadvisor.com'+foreurls+'Reviews-or'+str(10*i)+lasturl
            print(reviewurl)
            yield Request(reviewurl, callback=self.get_review,dont_filter=True)

    # collect all review
    def get_review(self, response):

        for i in range(1,10):
            item = TripadvisorItem()  # import item.py class

            # collect restaurant name, user name and review
            restaurantName =response.xpath("//*[@class='ui_header h1']/text()").extract()
            userName = response.xpath("//*[@class='info_text']//*/text()")[i].extract()
            review = response.xpath("//*[@class='partial_entry']/text()")[i].extract()

            item['restaurantName'] = restaurantName
            item['userName'] = userName
            item['review'] = review

            yield item






