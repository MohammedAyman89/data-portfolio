from scrapy.crawler import CrawlerProcess
import scrapy
import logging
import requests
import os
from scrapy.selector import Selector
from urllib.parse import urljoin, urlparse
# from imagescraper.items import ImagescraperItem

x = 1
class BridgewaterStateUniversityScraper(scrapy.Spider):
    name = 'washington-uni'

    def start_requests(self):
        url = 'https://www.washington.edu/students/crscat/'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//div[@class="col-md-8 uw-content"]/ul/li//a/@href').getall()
        for url in urls:
            if'#JSIS' in url:
                continue
            yield response.follow(url, callback=self.parse_courses)

    def parse_courses(self, response):
        for course_block in response.xpath('//p'):
            if course_block.xpath('./b/text()').get():
                course = {}
                
                course['code'] = ' '.join(course_block.xpath('./b/text()').get().strip().split(' ')[:2])
                course['title'] = ' '.join(course_block.xpath('./b/text()').get().strip().split(' ')[2:]).split('(')[0].strip()
                
                if course_block.xpath('./b/text()').get().strip().split(' ')[2][0].isnumeric():
                    course['code'] = ' '.join(course_block.xpath('./b/text()').get().strip().split(' ')[:3])
                    course['title'] = ' '.join(course_block.xpath('./b/text()').get().strip().split(' ')[3:]).split('(')[0].strip()

                
                course['credit'] = course_block.xpath('./b/text()').get().split('(')[1].split(')')[0].strip().split(',')[0].strip()
                if '*' in course['credit']:
                    course['credit'] = '0'
                
                if course_block.xpath('./text()').get():
                    course['description'] = course_block.xpath('./text()').get().replace('\n','').replace('\t','').replace('  ',' ')

                else:
                    course['description'] = ''
                yield course





    @staticmethod
    def normalize_spaces_and_line_breaks(text):
        # Replace line breaks with space
        text = text.replace('\n', ' ')

        # Replace multiple spaces with a single space
        text = ' '.join(text.split())

        return text


crawler = CrawlerProcess(settings={
    "FEEDS": {"uni1.csv": {"encoding": "utf8", "format": "csv", "overwrite": True}},
    "LOG_LEVEL": logging.INFO,
    "DOWNLOAD_DELAY": 1,
    "RANDOMIZE_DOWNLOAD_DELAY": 0.5,
    "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})
crawler.crawl(BridgewaterStateUniversityScraper)
crawler.start(stop_after_crawl=True)