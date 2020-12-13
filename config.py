# coding= UTF8


""" 
"af": "on", - На этапе подачи
"pa": "on", - Закупка отменена
"pc": "on", - Закупка завершена
"ca": "on", - Работа комиссии

"customerInn": "9201012877" - ФГАОУ ВО "Севастопольский Государственный Университет"

"delKladrIds": "8408975" - Место поставки Севастополь
"delKladrIds": "8408974" - Место поставки Крым

"priceFromGeneral": "30000000" - НМЦК от

"publishDateFrom": "11.12.2020" - дата публикации с

"""



URL = 'https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/extendedsearch/results.html'

headers = {'User-Agent': 'okhttp/3.12.1'}

params = {"fz44": "on", 
          "fz223": "on", 
          "ppRf615": "on", 
          "sortBy": "PUBLISH_DATE", 
          "recordsPerPage": '_100',  
          "pageNumber": "1"}
