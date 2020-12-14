# coding= UTF8


""" 
Запросы GET

purchases list
'https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/extendedsearch/results.html'

"af": "on", 					- На этапе подачи
"pa": "on", 					- Закупка отменена
"pc": "on", 					- Закупка завершена
"ca": "on", 					- Работа комиссии

"customerInn": "9201012877" 	- ФГАОУ ВО "Севастопольский Государственный Университет"

"delKladrIds": "8408975" 		- Место поставки Севастополь
"delKladrIds": "8408974" 		- Место поставки Крым

"priceFromGeneral": "30000000" 	- НМЦК от

"publishDateFrom": "11.12.2020" - дата публикации с

"updateDateFrom": "01.12.2020" 	- дата обновления с

"""

"""
purchase info
https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/common-info.html	- purchase info
https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/documents.html	- purchase document list
https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/journal.html		- purchase journal


protocols info
https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/protocols.html?regNumber=32009794727
https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/ok504/view/supplier-results.html?regNumber=0374500000520000112
https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/ok504/view/supplier-results.html?regNumber=0374500000520000112
https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/ea44/view/supplier-results.html?regNumber=0874200000120000585




"regNumber": "32009789894" - purchase number


"""
HOST = 'https://zakupki.gov.ru/api/mobile/proxy/917/'

SEARCH_URL = 'epz/order/extendedsearch/results.html'

HEADERS = {'User-Agent': 'okhttp/3.12.1'}

PARAMS = {"fz44": "on", 
          "fz223": "on", 
          "ppRf615": "on", 
          "sortBy": "UPDATE_DATE", 
          "recordsPerPage": '_100',  
          "pageNumber": "1"}


# Форматирование данных
"""
'stageNumber'
 'comments'
 'controlId'
 'createDate'
 'createDateAsTimestamp'
 'createDateMob'
 'currency'
 'currencyCbRate'
 'currencyContractCurrency'
 'currencyContractCurrencySymbol'
 'currencyRate'
 'currencyRateDate'
 'currencySymbol'
 'customerId'
 'customerName'
 'customerOrgType'
 'customers'
 'hasModificationClarification'
 'hasPlanGraph'
 'hasProtocol'
 'hasPublicDiscussion'
 'links'
 'linksWithUrls'
 'lotItems'
 'lotItemsTotal'
 'lots'
 'maxDateTimeZoneAbbrev'
 'maxPublishDate'
 'method'
 'methodType'
 'name'
 'nominalRate'
 'number'
 'okdpCode'
 'organization'
 'organizationId'
 'overhaulItemName'
 'pdiscNum'
 'placerOrgRole'
 'price'
 'priceContractCurrency'
 'printForm223Id'
 'printFormId'
 'provider'
 'purchaseNumbers'
 'recordId'
 'signViewUrl'
 'stage'
 'stagetStr'
 'startDate'
 'tillDate'
 'timeZoneAbbrev'
 'titleName'
 'titleNumber'
 'titleOrganization'
 'updateDate'
 'updateDateAsTimestamp'
 'updateDateMob'
 'manyPublishNotification'
 'multyLot'
 'ctrlInfosNotPass'
 'longPrice'
 'moreOneLot'
 'ctrlInfosPass'
 'currencyNotEquals'
 'parsePdiscNumToList'
 'cooperative'
 'centralized'
 'purchaseNumbersString'
 'blockedByUnschedInspect'
"""




need_keys = {'createDate', 'customers', 'hasProtocol', 
             'method', 'methodType', 'number', 
             'organization', 'price', 'provider', 
             'stagetStr', 'tillDate', 'timeZoneAbbrev', 
             'titleName', 'updateDate', 'customerOrgType'}

date_time_keys = {'createDate', 'createDateAsTimestamp',
                  'createDateMob', 'tillDate', 'updateDate',
                  'updateDateAsTimestamp', 'updateDateMob'}
