from scrapy.crawler import CrawlerProcess
import scrapy
import json 
import logging
from urllib.parse import urljoin, urlparse

class EvansvilleUniversity(scrapy.Spider):
    name = 'DAAD'

    @staticmethod
    def get_payload(pg_no):
        return json.dumps({"searchParameters":"{\"keyword\":null,\"terms\":[],\"requirement\":null,\"subrequirement\":null,\"courseIds\":null,\"sectionIds\":null,\"requirementText\":null,\"subrequirementText\":\"\",\"group\":null,\"startTime\":null,\"endTime\":null,\"openSections\":null,\"subjects\":[],\"academicLevels\":[],\"courseLevels\":[],\"synonyms\":[],\"courseTypes\":[],\"topicCodes\":[],\"days\":[],\"locations\":[],\"faculty\":[],\"onlineCategories\":null,\"keywordComponents\":[],\"startDate\":null,\"endDate\":null,\"startsAtTime\":null,\"endsByTime\":null,\"pageNumber\":"+str(pg_no)+",\"sortOn\":0,\"sortDirection\":0,\"subjectsBadge\":[],\"locationsBadge\":[],\"termFiltersBadge\":[],\"daysBadge\":[],\"facultyBadge\":[],\"academicLevelsBadge\":[],\"courseLevelsBadge\":[],\"courseTypesBadge\":[],\"topicCodesBadge\":[],\"onlineCategoriesBadge\":[],\"openSectionsBadge\":\"\",\"openAndWaitlistedSectionsBadge\":\"\",\"subRequirementText\":null,\"quantityPerPage\":30,\"openAndWaitlistedSections\":null,\"searchResultsView\":\"CatalogListing\"}"})

    def start_requests(self):
        # url = self._start_urls[0]
        url = 'https://selfservice.evansville.edu/Student/Courses'
        yield scrapy.Request(url, callback=self.parse)
    
    def parse(self, response):
        # Extract the cookies from the current response
        cookies = response.headers.getlist('Set-Cookie')[0].decode("utf-8").split(";")[0]
        url = "https://selfservice.evansville.edu/Student/Courses/PostSearchCriteria"
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json, charset=UTF-8',
            'Sec-Ch-Ua': '\\"Chromium\\";v=\\"110\\", \\"Not A(Brand\\";v=\\"24\\", \\"Google Chrome\\";v=\\"110\\"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '\\"Windows\\"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': cookies,
            'Referer': 'https://selfservice.evansville.edu/Student/Courses/Search',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            '__RequestVerificationToken': response.xpath('//input[@name="__RequestVerificationToken"]/@value').get()
            }

        # Pass the cookies to the next request using the meta dictionary
        yield scrapy.Request(url=url, method="POST", body="{\"keyword\":null,\"terms\":[],\"requirement\":null,\"subrequirement\":null,\"courseIds\":null,\"sectionIds\":null,\"requirementText\":null,\"subrequirementText\":\"\",\"group\":null,\"startTime\":null,\"endTime\":null,\"openSections\":null,\"subjects\":[],\"academicLevels\":[],\"courseLevels\":[],\"synonyms\":[],\"courseTypes\":[],\"topicCodes\":[],\"days\":[],\"locations\":[],\"faculty\":[],\"onlineCategories\":null,\"keywordComponents\":[],\"startDate\":null,\"endDate\":null,\"startsAtTime\":null,\"endsByTime\":null,\"pageNumber\":1,\"sortOn\":\"SectionName\",\"sortDirection\":\"Ascending\",\"subjectsBadge\":[],\"locationsBadge\":[],\"termFiltersBadge\":[],\"daysBadge\":[],\"facultyBadge\":[],\"academicLevelsBadge\":[],\"courseLevelsBadge\":[],\"courseTypesBadge\":[],\"topicCodesBadge\":[],\"onlineCategoriesBadge\":[],\"openSectionsBadge\":\"\",\"openAndWaitlistedSectionsBadge\":\"\",\"subRequirementText\":null,\"quantityPerPage\":5000,\"openAndWaitlistedSections\":null,\"searchResultsView\":\"CatalogListing\"}", headers=headers, callback=self.parse_result)

    def parse_result(self, response):
        # print(response.text)
        data = response.json()
        if data['CurrentPageIndex'] < data['TotalPages']:
            yield scrapy.Request(url="https://selfservice.evansville.edu/Student/Courses/PostSearchCriteria",dont_filter=True, method="POST", body=self.get_payload(data['CurrentPageIndex']+1), headers=response.request.headers, callback=self.parse_result)
        for course in data['CourseFullModels']:
            yield {
                'code': course['CourseTitleDisplay'],
                'title': course['Title'],
                'credit': course['CreditsCeusDisplay'],
                'description': course['Description']
            }





    @staticmethod
    def normalize_spaces_and_line_breaks(text):
        # Replace line breaks with space
        text = text.replace('\n', ' ')

        # Replace multiple spaces with a single space
        text = ' '.join(text.split())

        return text


crawler = CrawlerProcess(settings={
    "FEEDS": {"test1.csv": {"encoding": "utf8", "format": "csv", "overwrite": True}},
    "LOG_LEVEL": logging.INFO,
    "DOWNLOAD_DELAY": 1,
    "RANDOMIZE_DOWNLOAD_DELAY": 0.5,
    "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})
crawler.crawl(EvansvilleUniversity)
crawler.start(stop_after_crawl=True)

