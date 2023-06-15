from scrapy import Spider, Request
from scrapy.responsetypes import Response

from WebScraper.items import FiisscrapingItem, RendDistribution


class FiisScraperSpider(Spider):
    name = "fiis-scraper"
    allowed_domains = ["fundsexplorer.com.br"]
    
    format_file = 'json'
    custom_settings = {
        'FEEDS':{
            f'fiisdata.{format_file}': { 'format': format_file, 'overwrite': True}
        },
        'ITEM_PIPELINES': {
            "WebScraper.pipelines.FiisscrapingPipeline": 300,
        }
    }

    def __init__(self, fiis='', *args, **kwargs):
        super(FiisScraperSpider, self).__init__(*args, **kwargs)
        self.fiis = fiis

        self.start_urls = ["https://www.fundsexplorer.com.br/funds"]


    def parse(self, response: Response):
        for fii in self.fiis.split(','):

            url = f'https://www.fundsexplorer.com.br/funds/{fii}'
            type_css = f'.link-tickers-container[onclick="location.href=\'{url}\';"] span::text'
            fii_type = response.css(type_css).get()

            yield response.follow(url, callback=self.test, meta={'fii_type': fii_type})


    def test(self, response: Response):
        fii_type = response.meta['fii_type']

        fii_item = FiisscrapingItem()
        fii_item['url'] = response.url
        fii_item['fii_type'] = fii_type
        rend_distribution = RendDistribution()

        fii_item['name'] = response.css('.headerTicker__content__name::text').get()
        fii_item['code'] = response.css('.headerTicker__content__title::text').get()
        fii_item['status'] = response.css('.headerTicker__content__price span::text').get()
        fii_item['current_price'] = response.css('.headerTicker__content__price p::text').get()
        
        fii_data = response.css('.indicators:nth-child(1)')
        fii_item['average_daily'] = fii_data.css('.indicators__box:nth-child(1) p b::text').get()
        fii_item['last_dividend'] = fii_data.css('.indicators__box:nth-child(2) p b::text').get()
        fii_item['dividend_yield'] = fii_data.css('.indicators__box:nth-child(3) p b::text').get()
        fii_item['net_worth'] = fii_data.css('.indicators__box:nth-child(4) p b::text').get()
        fii_item['p_vp'] = fii_data.css('.indicators__box:nth-child(7) p b::text').get()
        
        fii_historic_data = response.css('.historic')
        fii_item['last_dividend_yield'] = fii_historic_data.css('div:nth-child(2) p:nth-child(2) b::text').get()

        last_rend_distribution = response.css('.communicated .communicated__grid .communicated__grid__rend') or None

        if last_rend_distribution is not None:
            rend_distribution['dividend'] = last_rend_distribution[0].css('p::text').get()
            rend_distribution['future_pay_day'] = last_rend_distribution[0].css('p::text').get()
            rend_distribution['income_percentage'] = last_rend_distribution[0].css('ul li:nth-child(3) b::text').get()
            rend_distribution['data_com'] = last_rend_distribution[0].css('ul li:nth-child(1) b::text').get()
            fii_item['rend_distribution'] = dict(rend_distribution)

        yield fii_item
