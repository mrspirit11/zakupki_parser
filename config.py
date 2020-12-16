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

NF 			- Извещение не размещено
AF 			- Подача заявок
CA 			- Работа комиссии
PC 			- Закупка завершена
PA 			- Закупка отменена
PO615 		- Предварительный отбор
EA615 		- Электронный аукцион 
NA 			- Определение поставщика отменено
NC 			- Определение поставщика завершено

purchase info
223
https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/common-info.html	- purchase info
44
https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/ok504/view/common-info.html
https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/ea44/view/common-info.html
https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/zp504/view/common-info.html

https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/documents.html	- purchase document list
https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/journal.html		- purchase journal


protocols info
https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/protocols.html
https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/ok504/view/supplier-results.html
https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/ok504/view/supplier-results.html
https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/ea44/view/supplier-results.html




"regNumber": "32009789894" - purchase number


"""
HOST = 'https://zakupki.gov.ru/api/mobile/proxy/917/'

SEARCH_URL = HOST + 'epz/order/extendedsearch/results.html'

PURCHASE_URLS = {'223': HOST + '223/purchase/public/purchase/info/common-info.html',
				 '44': HOST + 'epz/order/notice/{}/view/common-info.html'}

HEADERS = {'User-Agent': 'okhttp/3.12.1'}

PARAMS = {"fz44": "on", 
          "fz223": "on", 
          "ppRf615": "on", 
          "sortBy": "UPDATE_DATE", 
          "recordsPerPage": '_100',  
          "pageNumber": "1"}


# Форматирование данных

need_keys = {'createDate', 'method', 'methodType', 'number', 'price', 'provider', 
             'stagetStr', 'tillDate', 'titleName', 'updateDate', 'stage', 'customers', 'organization'}

date_time_keys = {'createDate', 'createDateAsTimestamp',
                  'createDateMob', 'tillDate', 'updateDate',
                  'updateDateAsTimestamp', 'updateDateMob'}


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


"""
Инфа по закупке

 'headerBlock':
Приостановлено по жалобе
'complaintsDto': {'complaintId': 2072527,
                  'complaintNumber': '202000100161005816',
                  'hasComplaint': True}

'organizationPublishName': 'ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ '
                                            'АВТОНОМНОЕ ОБРАЗОВАТЕЛЬНОЕ '
                                            'УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ '
                                            '"МОСКОВСКИЙ ГОСУДАРСТВЕННЫЙ '
                                            'ИНСТИТУТ МЕЖДУНАРОДНЫХ ОТНОШЕНИЙ '
                                            '(УНИВЕРСИТЕТ) МИНИСТЕРСТВА '
                                            'ИНОСТРАННЫХ ДЕЛ РОССИЙСКОЙ '
                                            'ФЕДЕРАЦИИ"',

'customerRequirementsBlock': list

Банковское сопровождение                 
{'bankSupportBlock': {'bankSupportType': 'NOT_REQUIRED',
                      'bankSupportTypeText': 'Банковское или казначейское 
                      						  сопровождение контракта не требуется'}

обеспечение заявок
'ensuringPurchase': {'amountEnforcement': 5258112.03,
                                                     'currency': 'Российский '
                                                                 'рубль',
                                                     'enforcementProcedure': 'В '
                                                                             'соответствии '
                                                                             'с '
                                                                             'документацией',
                                                     'offerGrnt': True,
                                                     'paymentRequisites': {'bik': '044525000',
                                                                           'ls': '05731001060',
                                                                           'rs': '40302810045251000079'},
                                                     'securityRequired': 'Требуется '
                                                                         'обеспечение '
                                                                         'заявок'},

обеспечение контракт
'ensuringPerformanceContract': {'additionalInformation': None,
                                                                'amountContractEnforcement': 52581120.27,
                                                                'contractGrntShare': 5,
                                                                'contractualSecurityRequired': 'Требуется '
                                                                                               'исполнения '
                                                                                               'контракта',
                                                                'currency': 'Российский '
                                                                            'рубль',
                                                                'energyServiceContract': False,
                                                                'enforcementProcedure': 'В '
                                                                                        'соответствии '
                                                                                        'с '
                                                                                        'документацией',
                                                                'offerGrnt': True,
                                                                'paymentRequisites': {'bik': '044525000',
                                                                                      'ls': '05731001060',
                                                                                      'rs': '40302810045251000079'},
                                                                'smpSono': False}                                                               эыьзЫщтщэЖ АфдыуЪб


"""





