from bs4 import BeautifulSoup as bs
import requests
from glob import glob
import tika.parser as t_p
import time, datetime
import re
import tabula
import os
import pandas

def get_doc_list(pages=2):
    """Return list of link to document from https://rk.gov.ru/
    pages=1 (one page), pages='all', default pages=4 """

    def get_html(page):
        url = 'https://rk.gov.ru/ru/documents/search'
        params = {'query':'Об определении единственного',
                  'dateFrom':'01.01.2020',
                  'page':page}
        return requests.get(url, params).text

    def a_list(pages):
        doc_list = []
        for page in range(1, pages + 1):
            soup = bs(get_html(page), 'html.parser')
            doc_ul = soup.find('ul', class_='search-results')
            a_list = doc_ul.findAll('a')
            doc_list.extend([a['href'] for a in a_list])
        return doc_list
    
    if pages == 'all':
        soup = bs(get_html(), 'html.parser')
        last_page_href = soup.find('li', class_='pagination__item_last').a['href']
        last_page_numb = int(last_page_href.split('=')[-1])
        return a_list(last_page_numb)
    else:
        return a_list(pages)

def download_all_pdf(link_list):
    def save_downloads(link):
        if 'downloads.txt' not in os.listdir('Downloads'):
            open('Downloads/downloads.txt', 'w').close()
        if link in open('Downloads/downloads.txt', 'r').read():
            return False
        else:
            open('Downloads/downloads.txt', 'a').write(f'{datetime.datetime.now()} - {link}\n')
            return True

    def download_pdf(link):
        url = 'https://rk.gov.ru'
        try:
            html_resp = requests.get(link)
            soup = bs(html_resp.text, 'html.parser')
            doc_info = soup.findAll('p')
            doc_name = doc_info[0].text.split()[-1].strip()
            doc_accept_date = doc_info[1].text.split()[-1].strip()
            doc_publ_date = doc_info[2].text.split()[-1].strip()
            doc_url = soup.find('a', class_='doc-name__link')['href']
            with open(f'Downloads/{doc_publ_date} {doc_name} от {doc_accept_date}.pdf', 'wb') as f_out:
                f_out.write(requests.get(url+doc_url).content)
        except IndexError:
            print(link)
        except requests.ConnectionError as e:
            print(e)
            time.sleep(2)
            download_pdf(link)

    for link in link_list:
        try:
            if save_downloads(link):
                download_pdf(link)
        except:
            continue

def get_text_from_pdf():
    file_list = glob('Downloads/*.pdf')
    out_list = []

    def find_and_clean(text, words):
        text = text.replace('https://rk.gov.ru/ru/document/show/21495', '')
        t_out = text[text.find(words[0])+ len(words[0]):text.find(words[1])].strip()
        return re.sub(r'\s+',' ', t_out)

    for file in file_list:
        purch_info = {}
        file_name = file[file.find('Downloads/') + len('Downloads/'):file.find('.pdf')]
        purch_info['file_name'] = file_name.split()
        pdf_file = t_p.from_file(file)
        numb_of_pages = int(pdf_file['metadata']['xmpTPg:NPages'])
        file_text = pdf_file['content'].strip()
        if numb_of_pages > 2:
            df = tabula.read_pdf(file, pages='all', lattice=True, multiple_tables=True)
            df = [i for i in df if len(i)>1]
            if len(df)>1:
                for i in df:
                    if len(i) > 1:
                        i.columns = df[0].columns
                        df1 = df[0].append(i, ignore_index=True)
            else:
                df1 = df[0]

            obj = df1.replace('\r',' ', regex=True)
            obj.columns = map(lambda s:s.replace('\r',' '), list(obj.columns))
            obj['Цена контракта (руб.)'] = obj['Цена контракта (руб.)'].replace(',','.', regex=True).replace(' ','', regex=True).astype("float")   

            purch_info['win_name'] = find_and_clean(file_text, ("1. Определить ", "единственным"))
            ensuringPerformanceContrac = find_and_clean(file_text, ("в размере ", "% от")).replace(',','.')
            purch_info['ensuringPerformanceContrac'] = ensuringPerformanceContrac if re.match(r'\b\d',ensuringPerformanceContrac) else None
            purch_info['obj'] = obj
            purch_info['price'] = 'В приложении'
            purch_info['zak'] = find_and_clean(file_text, ("заказчику", "заключить"))
            purch_info['zak'] = purch_info['zak'] if len(purch_info['zak']) < 500 else None
        else:
            purch_info['win_name'] = find_and_clean(file_text, ("1. Определить ", "единственным"))
            purch_info['obj'] = find_and_clean(file_text, ("является ", "(далее"))
            price = find_and_clean(file_text, ("ценой", "копе"))
            purch_info['price'] = float(''.join(re.findall(r'\d',price)))/100
            ensuringPerformanceContrac = find_and_clean(file_text, ("в размере ", "% от")).replace(',','.')
            purch_info['ensuringPerformanceContrac'] = ensuringPerformanceContrac if re.match(r'\b\d',ensuringPerformanceContrac) else None
            purch_info['zak'] = find_and_clean(file_text, ("заказчику", "заключить"))
            purch_info['zak'] = purch_info['zak'] if len(purch_info['zak']) < 500 else None
        out_list.append(purch_info)
        os.remove(file)
    return out_list

def to_html(data_list):
    start_html = """<!DOCTYPE html>
        <html>

        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
            <title>выгрузка ед поставщик</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/css/bootstrap.min.css">
            <link rel="stylesheet" href="assets/css/styles.min.css">
        </head>

        <body>"""
    end_html = """<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/js/bootstrap.bundle.min.js"></script></body></html>"""
    html = ''
    for data in data_list:
        if isinstance(data['obj'], pandas.core.frame.DataFrame):
            html += f"""    <div class="container">
                        <p><strong>{' '.join(data['file_name'][1:])}</strong></p>
                        <table class="table">
                    <tbody>
                        <tr>
                            <td>Размещено:</td>
                            <td>{data['file_name'][0]}</td>
                        </tr>
                    </tbody>
                </table>
                <table class="table">
                    <tbody>
                        <tr></tr>
                        <tr>
                            <td>Начальная цена контракта:</td>
                            <td><strong>{data['price']}</strong></td>
                        </tr>
                        <tr>
                            <td>Обеспечение контракта:</td>
                            <td><strong>{data['ensuringPerformanceContrac']}</strong></td>
                        </tr>
                    </tbody>
                </table>

                        <p>Заказчик: {data['zak']}</p>
                        <p><b>Победитель:</b> {data['win_name']}</p>
                            {data['obj'].to_html(classes="table", index=False, justify='left', 
                                float_format=lambda x: '{:,}'.format(x), col_space='20%',
                                columns=['Наименование объекта закупки', 'Цена контракта (руб.)'])}
                        </div>"""
        else:    
            html += f"""    <div class="container">
            <h1>{data['obj']}</h1>
                        <p><strong>{' '.join(data['file_name'][1:])}</strong></p><table class="table">
                    <tbody>
                        <tr>
                            <td>Размещено:</td>
                            <td>{data['file_name'][0]}</td>
                        </tr>
                    </tbody>
                </table>
                <table class="table">
                    <tbody>
                        <tr></tr>
                        <tr>
                            <td>Начальная цена контракта:</td>
                            <td><strong>{data['price']:,}</strong></td>
                        </tr>
                        <tr>
                            <td>Обеспечение контракта:</td>
                            <td><strong>{data['ensuringPerformanceContrac']}</strong></td>
                        </tr>
                    </tbody>
                </table>

                        <p>Заказчик: {data['zak']}</p>
                        <p><b>Победитель:</b> {data['win_name']}</p>
                        </div>"""
    return start_html + html + end_html

if __name__ == '__main__':
    download_all_pdf(get_doc_list(1))
    with open('test_rk.html', 'w') as f_out:
        f_out.write(to_html(get_text_from_pdf()))
    
