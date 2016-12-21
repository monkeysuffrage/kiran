import scrapy


class FederalReserveSpider(scrapy.Spider):
    name = 'federal-reserve-spider'
    start_urls = ['https://www.federalreserve.gov/releases/h10/hist/']

    def parse(self, response):
        for tr in response.css('.statistics tr'):
            href = tr.css('a[href]::attr(href)').extract_first()
            request = scrapy.Request(response.urljoin(href),
                                     callback=self.parse_link)
            request.meta['country'] = tr.css('a[href]::text').extract_first()
            request.meta['currency'] = tr.css('td::text').extract_first()
            yield request

    def parse_link(self, response):
        for tr in response.css('.statistics tr'):
            yield {
                'country': response.request.meta['country'],
                'currency': response.request.meta['currency'],
                'date': tr.css('th::text').extract_first().strip(),
                'rate': tr.css('td::text').extract_first().strip()
            }
