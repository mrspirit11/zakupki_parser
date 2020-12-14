import requests, json, html
from datetime import datetime
import pytz
from bs4 import BeautifulSoup as bs
import config

class parse_api():
    def __init__(self, params):
        self.params = dict(config.PARAMS)
        self.params.update(params)

    def get_json(self, url, **params):
        self.params.update(params)
        response = json.loads(requests.get(
            url,headers=config.HEADERS, params=self.params, verify=False).content)
        return response

    def format_data(self, json_data):

        def _clean_data(json_data):
            """Удаляет ненужные данные"""
            for item in json_data:
                list(map(item.pop, set(item.keys()) - config.need_keys))
                item['method'] = item['method']['name']
                item['titleName'] = html.unescape(item['titleName'])
                for customer in item['customers']:
                    del customer['id'], customer['anyFieldNull']

        def _unicode_time_convert(json_data):
            def time_format(timestamp, tz_info):
                if timestamp:
                    ts = int(timestamp)/1000
                    date = datetime.utcfromtimestamp(ts)
                    date = pytz.timezone("UTC").localize(date)
                    if tz_info:
                        tz = pytz.timezone(tz_info)
                        date = date.astimezone(tz)
                    else:
                        tz = pytz.timezone('Europe/Moscow')
                        date = date.astimezone(tz)

                    return date.strftime('%d-%m-%Y %H:%M:%S')

                else:
                    return timestamp

            for item in json_data:
                for key in item:
                    if key in config.date_time_keys:
                        item[key] = time_format(item[key], item['timeZoneAbbrev'])

        _clean_data(json_data)
        _unicode_time_convert(json_data)

        return json_data

    def get_purchases_list(self):
        url = config.HOST + config.SEARCH_URL
        json_data = self.get_json(url)
        items_data = json_data['data']['list']
        pageCount = json_data['data']['pagingDto']['pageCount']

        if pageCount > 1:
            page = 2
            while page <= pageCount:
                json_data = get_json(url, pageNumber=page)
                items_data.extend(json_data['data']['list'])
                page += 1
        return self.format_data(items_data)

    def get_protocol_info(self):
        pass

    def get_new_purchase(self):
        pass


if __name__ == "__main__":
    from pprint import pprint as pp
    import pandas

    krym_sevas_30kk = parse_api({"af": "on",
                                 "pa": "on",
                                 "pc": "on",
                                 "ca": "on",
                                 "delKladrIds": "8408974, 8408975",
                                 "updateDateFrom": "01.12.2020",
                                 "priceFromGeneral": 30000000})

    sev_gu = parse_api({"af": "on",
                        "pa": "on", 
                        "pc": "on",
                        "ca": "on",
                        "customerInn": "9201012877",
                        "updateDateFrom": "01.12.2020"})

    krym_sevas_df = pandas.DataFrame(krym_sevas_30kk.get_purchases_list())
    sev_gu_df = pandas.DataFrame(sev_gu.get_purchases_list())
    krym_sevas_df.to_excel('k_test.xlsx')
    sev_gu_df.to_excel('sev_gu_test.xlsx')

