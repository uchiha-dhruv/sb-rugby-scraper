import scrapy


class LinkSpider(scrapy.Spider):
    name = 'test'
    start_urls = [
        'https://rugby.statbunker.com/competitions/LastMatches?comp_id=646&limit=10&offs=UTC&offset=',
        'https://rugby.statbunker.com/competitions/LastMatches?comp_id=646&limit=10&offs=UTC&offset=10',
        'https://rugby.statbunker.com/competitions/LastMatches?comp_id=646&limit=10&offs=UTC&offset=20',
        'https://rugby.statbunker.com/competitions/LastMatches?comp_id=646&limit=10&offs=UTC&offset=30',
        'https://rugby.statbunker.com/competitions/LastMatches?comp_id=646&limit=10&offs=UTC&offset=40'
    ]

    def parse(self, response):
        match_links = response.css(".matchStatLink a::attr(href)").extract()

        for link in match_links:
            yield {
                'Link': link
            }

        # next_page = response.css(".pagination li a::attr(href)").get()
        # if next_page is not None:
        # for href in response.css(".pagination li a::attr(href)"):
        # yield response.follow(href, callback=self.parse)
        # for x in range(10, 150, 10):
        #     next_page = response.url + str(x)
        #     yield response.follow(next_page, callback=self.parse)
