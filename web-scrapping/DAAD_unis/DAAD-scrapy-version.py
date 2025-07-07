from scrapy.crawler import CrawlerProcess
import scrapy
import logging
from urllib.parse import urljoin, urlparse

class BridgewaterStateUniversityScraper(scrapy.Spider):
    name = 'DAAD'

    def start_requests(self):
        url = "https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json?cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&degree%5B%5D=1&fos=&langDeAvailable=&langEnAvailable=&lang%5B%5D=4&fee=&sort=4&dur=&q=&limit=100&offset=&display=list&isElearning=&isSep="
        
        headers = {
                        "accept": "application/json, text/plain, */*",
                        "accept-language": "en-US,en;q=0.9",
                        "priority": "u=1, i",
                        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": "\"Windows\"",
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin",
                        "cookie": "daad_cookie_consent={\"availableCookies\":[\"google-analytics\",\"sticky-alert\",\"session\",\"daad-cookie-consent\"],\"acceptedCookies\":[\"google-analytics\",\"sticky-alert\",\"session\",\"daad-cookie-consent\"],\"lastUpdated\":1751886783628}; _ga=GA1.1.1164999859.1751886784; _ga_ZGGH7Q9DE9=GS2.1.s1751891201$o2$g0$t1751891203$j58$l0$h0",
                        "Referer": "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/?q=&degree%5B%5D=1&lang%5B%5D=4&fos=&cert=&admReq=&langExamPC=&scholarshipLC=&langExamLC=&scholarshipSC=&langExamSC=&langDeAvailable=&langEnAvailable=&modStd%5B%5D=&cit%5B%5D=&tyi%5B%5D=&ins%5B%5D=&fee=&bgn%5B%5D=&dat%5B%5D=&prep_subj%5B%5D=&prep_degree%5B%5D=&sort=4&dur=&subjects%5B%5D=&limit=100&offset=&display=list"
                    }
        yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        college_data = response.json()
        data = college_data['courses']
        for data1 in data:
            program = {}
            program['program_ID'] = data1['id']
            program['program_name'] = data1['courseNameShort']
            program['subject'] = data1['subject']
            program['city'] = data1['city']
            program['language'] = data1['languages']
            program['Duration'] = data1['programmeDuration']
            program['fees'] = data1['tuitionFees']
            yield program





    @staticmethod
    def normalize_spaces_and_line_breaks(text):
        # Replace line breaks with space
        text = text.replace('\n', ' ')

        # Replace multiple spaces with a single space
        text = ' '.join(text.split())

        return text


crawler = CrawlerProcess(settings={
    "FEEDS": {"DAAD-scrapy.csv": {"encoding": "utf8", "format": "csv", "overwrite": True}},
    "LOG_LEVEL": logging.INFO,
    "DOWNLOAD_DELAY": 1,
    "RANDOMIZE_DOWNLOAD_DELAY": 0.5,
    "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})
crawler.crawl(BridgewaterStateUniversityScraper)
crawler.start(stop_after_crawl=True)

