import scrapy
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AngelInvestorsSpider(CrawlSpider):
    name = "angelinvestors1"
    allowed_domains = ["shizune.co"]
    start_urls = ['https://shizune.co/investors/fintech-angel-investors-nigeria']

    # crawling
    rules = (
        Rule(
            LinkExtractor(
                restrict_css='a',  # CSS selector for the div containing links
            ),
            callback='parse_item',
            follow=True,
        ),
    )

    def parse_item(self, response):
        yield {
            "twitter_links": response.css('a[href*="twitter.com"]::attr(href)').get(),
            "facebook_links": response.css('a[href*="facebook.com"]::attr(href)').get(),
            "linkedin_links": response.css('a[href*="linkedin.com"]::attr(href)').get(),
            "name": response.css(".investor__name::text").get(),
            "description": response.css(".desc::text").get()
        }

# Run the spider and output the data to output.json
output_file = "output.json"
process = scrapy.crawler.CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'FEED_FORMAT': 'json',
    'FEED_URI': output_file
})
process.crawl(AngelInvestorsSpider)
process.start()
