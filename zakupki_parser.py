import requests, json
from datetime import datetime
from bs4 import BeautifulSoup as bs
import config

class parse_api():
    def __init__(self, params):
        self.params = params

    def get_json(self):

        def _unicode_time_convert(timestamp):
            if timestamp:
                ts = int(timestamp)/1000
                return datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
            else:
                return timestamp
        items_data = []

        response = json.loads(requests.get(
            config.URL,headers=config.headers, params=self.params).content)

        items_data.extend(response['data']['list'])
        pageCount = response['data']['pagingDto']['pageCount']
        if pageCount > 1:
            page = 2
            while page <= pageCount:
                self.params['pageNumber'] = page
                response = json.loads(requests.get(
                                config.URL,headers=config.headers, params=self.params).content)
                items_data.extend(response['data']['list'])
                # print(response['data']['pagingDto'])
                page += 1

        date_time_keys = ('createDate', 'createDateAsTimestamp',
                          'createDateMob', 'tillDate', 'updateDate',
                          'updateDateAsTimestamp', 'updateDateMob')

        for key in date_time_keys:
            for item in items_data:
                item[key] = _unicode_time_convert(item[key])

        return items_data

    def get_purchase_info(self):
        pass 

    def get_protocol_info(self):
        pass

    def get_new_purchase(self):
        pass


if __name__ == "__main__":
    from pprint import pprint as pp
    import pandas
    krym_30kk = {"af": "on",
                 "pc": "on",
                 "delKladrIds": "8408974",
                 "publishDateFrom": "01.12.2020",
                 "priceFromGeneral": "3000000"}

    krym_params = dict(config.params)
    krym_params.update(krym_30kk)
    krym = parse_api(krym_params)
    purc_list = krym.get_json()
    # pp(len(purc_list))

    df = pandas.DataFrame(purc_list)
    df.to_excel('test.xlsx')
