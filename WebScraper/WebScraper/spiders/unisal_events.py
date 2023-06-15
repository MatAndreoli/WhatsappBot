import json
import scrapy
from scrapy.responsetypes import Response
from scrapy.http import TextResponse
from WebScraper.items import UnisaleventsItem

class UnisalEventsSpider(scrapy.Spider):
    name = "unisal-events"

    format_file = 'json'
    custom_settings = {
        'FEEDS':{
            f'events.{format_file}': { 'format': format_file, 'overwrite': True}
        },
        'ITEM_PIPELINES': {
            "WebScraper.pipelines.UnisalEventsPipeline": 300,
        }
    }

    def __init__(self, fiis='', *args, **kwargs):
        super(UnisalEventsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://unisal.br/wp-admin/admin-ajax.php?action=jet_smart_filters&provider=jet-engine%2Feventos&defaults%5Bpost_status%5D%5B%5D=publish&defaults%5Bpost_type%5D=eventos-unisal&defaults%5Bposts_per_page%5D=6&defaults%5Bpaged%5D=1&defaults%5Bignore_sticky_posts%5D=1&settings%5Blisitng_id%5D=4108&settings%5Bcolumns%5D=2&settings%5Bcolumns_tablet%5D=&settings%5Bcolumns_mobile%5D=1&settings%5Bpost_status%5D%5B%5D=publish&settings%5Buse_random_posts_num%5D=&settings%5Bposts_num%5D=6&settings%5Bmax_posts_num%5D=9&settings%5Bnot_found_message%5D=No+data+was+found&settings%5Bis_masonry%5D=&settings%5Bequal_columns_height%5D=&settings%5Buse_load_more%5D=&settings%5Bload_more_id%5D=&settings%5Bload_more_type%5D=click&settings%5Bload_more_offset%5D%5Bunit%5D=px&settings%5Bload_more_offset%5D%5Bsize%5D=0&settings%5Bloader_text%5D=&settings%5Bloader_spinner%5D=&settings%5Buse_custom_post_types%5D=&settings%5Bcustom_post_types%5D=&settings%5Bhide_widget_if%5D=&settings%5Bcarousel_enabled%5D=&settings%5Bslides_to_scroll%5D=1&settings%5Barrows%5D=true&settings%5Barrow_icon%5D=fa+fa-angle-left&settings%5Bdots%5D=&settings%5Bautoplay%5D=true&settings%5Bautoplay_speed%5D=5000&settings%5Binfinite%5D=true&settings%5Bcenter_mode%5D=&settings%5Beffect%5D=slide&settings%5Bspeed%5D=500&settings%5Binject_alternative_items%5D=&settings%5Bscroll_slider_enabled%5D=&settings%5Bscroll_slider_on%5D%5B%5D=desktop&settings%5Bscroll_slider_on%5D%5B%5D=tablet&settings%5Bscroll_slider_on%5D%5B%5D=mobile&settings%5Bcustom_query%5D=&settings%5Bcustom_query_id%5D=&settings%5B_element_id%5D=eventos&settings%5Bjet_cct_query%5D=&props%5Bfound_posts%5D=56&props%5Bmax_num_pages%5D=10&props%5Bpage%5D=2&paged={i + 1}" for i in range(10)]


    def parse(self, response: Response):
        tt = json.loads(response.text)

        text_response = TextResponse(url=response.url, body=tt['content'], encoding='utf-8')

        cards = text_response.css('.jet-listing-grid__items .jet-listing-grid__item')

        for card in cards:
            unisal_events = UnisaleventsItem()

            unisal_events['title'] = card.css('.elementor-heading-title::text').get()
            unisal_events['link'] = card.css('.elementor-size-xs::attr(href)').get()
            unisal_events['date'] = card.css('.elementor-inline-item:nth-child(1) .elementor-icon-list-text::text').get()
            unisal_events['hour'] = card.css('.elementor-inline-item+ .elementor-inline-item .elementor-icon-list-text::text').get()
            
            yield unisal_events
