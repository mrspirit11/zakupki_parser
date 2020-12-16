import requests, json, html, urllib3
from datetime import datetime
import pytz, re
from bs4 import BeautifulSoup as bs
import config

urllib3.disable_warnings()

class parse_api():
    def __init__(self, params):
        self.params = dict(config.PARAMS)
        self.params.update(params)

    def get_json(self, url, **params):
        self.params.update(params)
        ch = True
        while ch:
            try:
                response = json.loads(requests.get(
                    url,headers=config.HEADERS, params=self.params, verify=False).content)
                ch = False
            except requests.exceptions.ConnectionError as e:
                print(e)
        return response

    def format_data(self, json_data):

        def _clean_data(json_data):
            """Удаляет ненужные данные"""
            for item in json_data:
                item['method'] = item['method']['name']
                item['titleName'] = re.sub(r'\s{2}', ' ', html.unescape(item['titleName']))
                list(map(item.pop, set(item.keys()) - config.need_keys))

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

        _unicode_time_convert(json_data)
        _clean_data(json_data)

        return json_data

    def get_purchases_list(self):
        json_data = self.get_json(config.SEARCH_URL)
        items_data = json_data['data']['list']
        pageCount = json_data['data']['pagingDto']['pageCount']

        if pageCount > 1:
            page = 2
            while page <= pageCount:
                json_data = get_json(url, pageNumber=page)
                items_data.extend(json_data['data']['list'])
                page += 1
        self.purchases_list = self.format_data(items_data)
        for purchase in self.purchases_list:
            if '44' in purchase['provider']:
                purch_info = self.get_purchase_info(purchase['number'], purchase['provider'], purchase['methodType'])
                purchase.update(self.format_purchase_info_44(purch_info))
            
        return self.purchases_list

    def get_purchase_info(self, purchase_numb, provider, methodType):
        if provider == 'FZ223':
            print(purchase_numb)
            return self.get_json(config.PURCHASE_URLS['223'], regNumber=purchase_numb)['data']
        url = config.PURCHASE_URLS['44'].format(methodType.lower())
        print(url, purchase_numb)
        purch_info = self.get_json(url, regNumber=purchase_numb)['data']['dto']
        return purch_info
        
    def format_purchase_info_44(self, json_data):
        if json_data:
            purchase_info = {
            'complaints': json_data['headerBlock']['complaintsDto']['complaintNumber'],
            'ensuringPurchase' : json_data['customerRequirementsBlock'][0]['ensuringPurchase']['amountEnforcement'],
            'ensuringPerformanceContrac' : json_data['customerRequirementsBlock'][0]['ensuringPerformanceContract']['amountContractEnforcement']
            }
            return purchase_info


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
    # krym_sevas_30kk.get_purchases_list()
    # pp(krym_sevas_30kk.purchases_list)

