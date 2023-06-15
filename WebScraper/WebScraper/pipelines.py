import re
import datetime
from itemadapter import ItemAdapter


class UnisalEventsPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fields = adapter.field_names()
        for field in fields:
            if field == 'date':
                pattern = re.compile('^(\d+[\/|\.]\d+[\/|\.]\d+)$')

                if pattern.match(adapter.get(field)):
                    adapter[field] = '/'.join(re.split('[\/|\.]', adapter.get(field))[::-1])
                
                if ' à ' in adapter.get(field):
                    adapter['dates'] = adapter.get(field)
                    adapter[field] = str(datetime.date.today().year) + '/' + '/'.join(re.split('[\/|\.]', adapter.get(field).split(' ')[0])[::-1])

        return item


class FiisscrapingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fields = adapter.field_names()

        for field in fields:
            field_type = type(adapter.get(field))

            if field_type is str:
                adapter[field] = adapter.get(field).strip()

            elif field_type is list:
                for value in adapter.get(field):
                    strip_dict_values(value)

            elif field_type is dict:
                strip_dict_values(adapter.get(field))


            if field == 'dividend_yield':
                adapter[field] += '%'
            
            if field == 'last_dividend':
                adapter[field] = 'R$ ' + adapter.get(field)

        return item

def strip_dict_values(dict):
    for key in dict.keys():
        dict[key] = dict.get(key).strip()
        if key == 'dividend':
            dict[key] = re.findall('R\$\s[\d+]+\,\d+', dict[key])[0]
        if key == 'future_pay_day':
            dict[key] = re.findall('(\d+\/\d+\/\d+)+', dict[key])[0]
