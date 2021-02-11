# coding: utf-8

from bs4 import BeautifulSoup as bs
import requests, feedparser, re
from datetime import datetime, timedelta
import config



def get_date_from():
    date_format = "%d.%m.%Y"
    today = datetime.now()

    if today.weekday() == 0:
        date_from = today - timedelta(days=3)
    else:
        date_from = today - timedelta(days=1)
    date = date_from.strftime(date_format)
    print(date)
    return date


URL = 'https://zakupki.gov.ru/epz/contract/search/rss'

PARAMS = {'morphology':'on',
          'search-filter':'Дате+размещения',
          'fz44':'on',
          'contractStageList_0':'on',
          'contractStageList':0,
          'contractCurrencyID':-1,
          'countryRegIdNameHidden':'%7B%7D&',
          'budgetLevelsIdNameHidden':'%7B%7D',
          'publishDateFrom':get_date_from(),
          'placingWayList':'EP44%2CEPP44%2CINM111%2CINMP111%2CEP111',
          'selectedLaws':'FZ44',
          'sortBy':'PUBLISH_DATE',
          'pageNumber':1,
          'sortDirection':'false',
          'recordsPerPage':'_10',
          'showLotsInfoHidden':'false'}

SEV_PARAMS = {'customerPlace':8408975}
KRYM_PARAMS = {'customerPlace':8408974}


def get_contracts_urls(params):
    rss_resp = requests.get(URL, params=PARAMS, headers=config.HEADERS)
    contracts_url = ['https://zakupki.gov.ru' + item['link'] for item in feedparser.parse(rss_resp.text)['entries']]

def zak_cotracts_parse(url_list):
    count = len(url_list)
    info = []
    for url in url_list:
        print(count, end=', ')
        count -= 1

        html = requests.get(url, headers=config.HEADERS).text
        soup = bs(html, "html.parser")
        try:
            osnov = soup.find(
                'span', text='Основание заключения контракта с единственным поставщиком').parent()
            osnov = [re.sub(r'[\n ]+', ' ', item.text) for item in osnov]

            if 'Республики Крым' in osnov[1]:

                contr_name = soup.find('span', text='Предмет контракта')
                if contr_name :
                    contr_name = contr_name.parent()[1].text
                else:
                    contr_name=soup.find('span', class_ = 'text-break').text
                contr_name=re.sub(r'[\n ]+', ' ', contr_name)

                contr_info = [re.sub(
                    r'[\n ]+', ' ', soup.findAll('span', class_='cardMainInfo__content')[0].text),
                    re.sub(
                    r'[\n ]+', ' ', soup.findAll('span', class_='cardMainInfo__content')[1].text), 
                    contr_name,
                    re.sub(
                    r'[\n ]+', ' ', soup.find('span', text='Размещен контракт в реестре контрактов').parent()[1].text),
                    re.sub(
                    r'[\n ]+', ' ', soup.find('div', class_='price').text)]

                osnov_doc = soup.find(
                    'span', text='Реквизиты документа, подтверждающего основание заключения контракта')
                if osnov_doc:
                    osnov_doc = [re.sub(r'[\n ]+', ' ', item.text)
                                for item in osnov_doc.parent()]
                else:
                    osnov_doc = ''
                vendor_info = soup.find(
                    'h2', text='Информация о поставщиках').parent()[1]
                vendor_info = [td for td in vendor_info.findAll('td')][0]
            
                info.append({'contr_info': contr_info,
                            'osnov': osnov, 
                            'osnov_doc': osnov_doc, 
                            'vendor_info': vendor_info,
                            'url': url})
        except Exception as e:
            print(e, url)
    return info

PARAMS.update(SEV_PARAMS)

def main():
    contracts_list = get_contracts_urls(PARAMS)
    print(contracts_list)
    try:
        html = '<head><meta charset="utf-8"></head>'
        main_info = zak_cotracts_parse(contracts_list)
        for i in main_info:
            html += f"""
                <h3><a href="{i['url']}">{i['contr_info'][2]}<br>{i['url'].split('=')[1]}</a></h3>
                Размещен в реестре контрактов:<br>
                {i['contr_info'][-2]}<br><br>
                <h3>{i['contr_info'][-1]}</h3>
                {i['contr_info'][0]}<br><br>
                <!--{'<br>'.join(i['osnov'])}<br><br> -->
                {'<br>'.join(i['osnov_doc'])}<br><br>
                {i['vendor_info']}<br><br>
                {'*'*50}<br>"""

        if html:
            with open('ed_sevas.html', 'w', encoding='UTF-8') as f_out:
                f_out.write(html)
    except: pass

