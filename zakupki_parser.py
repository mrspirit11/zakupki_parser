import requests, json, html, urllib3
from datetime import datetime, timedelta
import pytz, re
from bs4 import BeautifulSoup as bs
import time
import config

urllib3.disable_warnings()

class parse_api():
    def __init__(self, params):
        self.params = dict(config.PARAMS)
        if "updateDateFrom" not in params.keys():
            params["updateDateFrom"] = self.get_date_from()
        self.params.update(params)

    def get_json(self, url, **params):
        ch = True
        while ch:
            try:
                response = requests.get(url,
                                        headers=config.HEADERS, 
                                        params=params, 
                                        verify=False)
                print(response.url)
                resp_json = json.loads(response.content)
                ch = False
            except requests.exceptions.ConnectionError as e:
                print(e)
                time.sleep(10)
        return resp_json

    def format_data(self, json_data):

        def _clean_data(json_data):
            """Удаляет ненужные данные"""
            for item in json_data:

                if item['method']:
                    item['method'] = item['method']['name']

                item['titleName'] = re.sub(r'\s{2}', ' ', html.unescape(item['titleName']))

                for lot in item['lotItems']:
                    list(map(lot.pop, set(lot.keys()-{'firstPrice', 'id', 'name', 'number'})))

                if not item['price']:
                    item['price'] = sum([i['firstPrice'] for i in item['lotItems']])

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
        self.params['pageNumber'] = 1
        json_data = self.get_json(config.SEARCH_URL, **self.params)
        items_data = json_data['data']['list']
        pageCount = json_data['data']['pagingDto']['pageCount']

        if pageCount > 1:
            page = 2
            while page <= pageCount:
                self.params['pageNumber'] = page
                json_data = self.get_json(config.SEARCH_URL, **self.params)
                items_data.extend(json_data['data']['list'])
                page += 1
        self.purchases_list = self.format_data(items_data)

        len_purch_list = len(self.purchases_list)

        for purchase in self.purchases_list:
            print(len_purch_list, end=', ')
            purch_info = self.get_purchase_info(purchase['number'], purchase['provider'], purchase['methodType'])
            purchase.update(purch_info)
            len_purch_list -= 1
            

        return self.purchases_list

    def get_purchase_info(self, purchase_numb, provider, methodType):

        if '223' in provider:
            purch_info = self.get_json(config.PURCHASE_URLS['223'], regNumber=purchase_numb)['data']
            purchase_info = {'customers':[{'inn': purch_info['noticeInfo']['customerInn'],
                                           'name': purch_info['noticeInfo']['customerName']}]
                             }
            return purchase_info

        if '615' in provider:
            url = config.PURCHASE_URLS['615'].format(methodType.lower())
            purch_info = self.get_json(url, regNumber=purchase_numb)['data']['dto']
            purchase_info = {
                    'complaints': purch_info['headerBlock']['complaintsDto']['complaintNumber'],
                    'ensuringPurchase' : purch_info['conditionsContract']['amountCollateralEA'],
                    'ensuringPerformanceContrac' : purch_info['conditionsContract']['amountCollateralContract']
                    }

            return purchase_info
        if '44' in provider:
            url = config.PURCHASE_URLS['44'].format(methodType.lower())
            purch_info = self.get_json(url, regNumber=purchase_numb)['data']['dto']
            purchase_info = {
                    'complaints': purch_info['headerBlock']['complaintsDto']['complaintNumber'],
                    'ensuringPurchase' : purch_info['customerRequirementsBlock'][0]['ensuringPurchase']['amountEnforcement'],
                    'ensuringPerformanceContrac' : purch_info['customerRequirementsBlock'][0]['ensuringPerformanceContract']['amountContractEnforcement'],
                    'contractGrntShare':purch_info['customerRequirementsBlock'][0]['ensuringPerformanceContract']['contractGrntShare'],
                    'warrantyObligationsSize':purch_info['customerRequirementsBlock'][0]['warrantyObligations']['warrantyObligationsSize']
                    }
            try:
                prot_url = config.PROTOCOL_URLS['44'].format(methodType.lower())
                prot_info = self.get_json(prot_url, regNumber=purchase_numb)['data']['dto']
                for prot in prot_info['protocolResultCommonBlock'][0]['protocolResults']:
                    if 0 < len(prot['reason']) < 20:
                        purchase_info[prot['reason'][4:]] = prot['partiicipantName']
                        purchase_info[prot['reason'][4:]+' предл'] = prot['offerPrice']
                    else:
                        if prot['reason']:
                            purchase_info['reason'] = prot['reason']
                        if prot['partiicipantName']:
                            purchase_info['Победитель'] = prot['partiicipantName']
                        purchase_info['Победитель предл'] = prot['offerPrice']

            except:
                pass
            return purchase_info

    def get_date_from(self):
        date_format = "%d.%m.%Y"
        today = datetime.now()

        if today.weekday() == 0:
            date_from = today - timedelta(days=3)
        else:
            date_from = today - timedelta(days=1)

        return date_from.strftime(date_format)



if __name__ == "__main__":
    from pprint import pprint as pp
    import pandas

    krym_sevas_30kk = parse_api({
                                 # "af": "on",
                                 # "pa": "on",
                                 "pc": "on",
                                 # "ca": "on",
                                 "fz44": "on", 
                                 # "fz223": "on", 
                                 "ppRf615": "on",
                                 'updateDateFrom':'01.12.2020',
                                 "delKladrIds": "8408974, 8408975",
                                 "priceFromGeneral": 30000000})

    sev_gu = parse_api({"af": "on",
                        "pa": "on", 
                        "pc": "on",
                        "ca": "on",
                        'updateDateFrom':'23.12.2020',
                        "customerInn": "9201012877"})

    krym_sevas_df = pandas.DataFrame(krym_sevas_30kk.get_purchases_list())
    # sev_gu_df = pandas.DataFrame(sev_gu.get_purchases_list())
    krym_sevas_df.to_excel('k_test.xlsx')
    # sev_gu_df.to_excel('sev_gu_test.xlsx')

