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
    name = 'Gaza-Israel War'

    def start_requests(self):
        url = 'https://www.bbc.com/news/topics/c2vdnvdg6xxt'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//section[@data-testid="virginia-section-outer-7"]//div[@class="sc-d2e835e5-1 jXwfPV"]//div[@data-testid="anchor-inner-wrapper"]/a/@href').getall()
        for url in urls:
            yield response.follow(url, callback=self.parse_title)

    def parse_title(self, response):
        news = {}
        news['title'] = response.xpath('//div[@data-component="headline-block"]/h1/text()').get()
        news['link'] = response.url
        news['article'] = ''.join(response.xpath('//div[@data-component="text-block"]//text()').getall()).strip()
        
        # Get image URL
        image_urls = response.xpath('//div[@class="sc-d1200759-1 kycbVO"]/img/@src').getall()
        if len(image_urls) > 1:
            image_url = image_urls[1]
        elif len(image_urls) > 0:
            image_url = image_urls[0]
        else:
            # Fallback to other image selectors
            image_url = response.xpath('//img[contains(@class, "media")]/@src').get()
        
        if image_url:
            # Make sure we have a complete URL
            if image_url.startswith('//'):
                image_url = 'https:' + image_url
            elif image_url.startswith('/'):
                image_url = urljoin(response.url, image_url)
            
            # Download and save the image
            image_filename = self.download_image(image_url, news['title'])
            news['image_url'] = image_url
            news['image_filename'] = image_filename
        else:
            news['image_url'] = ''
            news['image_filename'] = ''
        
        yield news

    def download_image(self, image_url, title):
        """Download image and save it to the images directory"""
        try:
            # Create images directory if it doesn't exist
            if not os.path.exists('images'):
                os.makedirs('images')
            
            # Clean title for filename
            clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_title = clean_title.replace(' ', '_')[:50]  # Limit filename length
            
            # Get file extension from URL
            parsed_url = urlparse(image_url)
            file_ext = os.path.splitext(parsed_url.path)[1]
            if not file_ext:
                file_ext = '.jpg'  # Default extension
            
            filename = f"{clean_title}{file_ext}"
            filepath = os.path.join('images', filename)
            
            # Download the image
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filename
        except Exception as e:
            self.logger.error(f"Failed to download image {image_url}: {str(e)}")
            return ''




    @staticmethod
    def normalize_spaces_and_line_breaks(text):
        # Replace line breaks with space
        text = text.replace('\n', ' ')

        # Replace multiple spaces with a single space
        text = ' '.join(text.split())

        return text


crawler = CrawlerProcess(settings={
    "FEEDS": {"BBC_news.csv": {"encoding": "utf8", "format": "csv", "overwrite": True}},
    "LOG_LEVEL": logging.INFO,
    "DOWNLOAD_DELAY": 1,
    "RANDOMIZE_DOWNLOAD_DELAY": 0.5,
    "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})
crawler.crawl(BridgewaterStateUniversityScraper)
crawler.start(stop_after_crawl=True)