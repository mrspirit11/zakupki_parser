# coding= UTF8

HOST = 'https://zakupki.gov.ru/api/mobile/proxy/917/'

SEARCH_URL = HOST + 'epz/order/extendedsearch/results.html'

PURCHASE_URLS = {'223': HOST + '223/purchase/public/purchase/info/common-info.html',
                 '44': HOST + 'epz/order/notice/{}/view/common-info.html',
                 '615': HOST + 'epz/order/notice/{}/view/common-info.html'}

PROTOCOL_URLS = {'44': HOST + 'epz/order/notice/{}/view/supplier-results.html',
                 '615': HOST + 'epz/order/notice/{}/view/supplier-results.html'}

HEADERS_MOBILE = {'User-Agent': 'okhttp/3.12.1'}
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36'}

PARAMS = {"sortBy": "UPDATE_DATE", 
          "recordsPerPage": '_100',  
          "pageNumber": "1"}


# Форматирование данных

need_keys = {'createDate', 'method', 'methodType', 'number', 'price', 'provider', 'stagetStr', 'tillDate', 
             'titleName', 'updateDate', 'stage', 'customers', 'organization', 'lotItems', 'lotItemsTotal'}

date_time_keys = {'createDate', 'createDateAsTimestamp','createDateMob', 'tillDate', 'updateDate',
                  'updateDateAsTimestamp', 'updateDateMob'}


# html
HTML_START = """<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>выгрузка</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/styles.min.css">
</head>

<body>"""
HTML_TEXT = """ <div class="container">
<h1><a href="{href}" target="_blank">{titleName}</a><br><strong>№ {number}</strong></h1>
        <p>{provider}, {method}</p>
            <table class="table">
              <tbody>
                  <tr>
                      <td>Обновлено:</td>
                      <td>{updateDate}</td>
                  </tr>
                  <tr>
                      <td>Этап закупки:&nbsp;</td>
                      <td><strong>{stagetStr}</strong></td>
                  </tr>
                  <tr>
                      <td>Подача заявки:</td>
                      <td>{createDate}<br>{tillDate}</td>
                  </tr>
              </tbody>
            </table>
            <table class="table">
              <tbody>
                  <tr>
                      <td>Начальная цена контракта:</td>
                      <td><strong>{price:,} &#8381</strong></td>
                  </tr>
                  <tr>
                      <td>Обеспечение заявки:</td>
                      <td><strong>{ensuringPurchase:,} &#8381</strong></td>
                  </tr>
                  <tr>
                      <td>Обеспечение контракта:</td>
                      <td><strong>{ensuringPerformanceContrac:,} &#8381; {contractGrntShare}%</strong></td>
                  </tr>
                  <tr>
                      <td>Обеспечение гарантийных:</td>
                      <td><strong>{warrantyObligationsSize:,} &#8381</strong></td>
                  </tr>
              </tbody>
            </table>
        <p>{organization}</p>"""
HTML_WIN = """
            <table class="table">
              <thead>
                  <tr>Победитель</tr>
              </thead>
              <tbody>
                <tr>
                    <td><b>{1 - Победитель}</b></td>
                    <td><strong>{1 - Победитель - предл:,} &#8381</strong></td>
                </tr>
                <tr></tr>
              </tbody>
            </table>
        """
HTML_COMM = '<p><em>{коммент}</em></p>'
HTML_COMPL = """<div class="alert alert-success" role="alert">
                <span style="color: rgb(0,0,0);"><strong>Жалобы:</strong><br>
                <a href="{href}" target="_blank">{complaints}</a></span></div>"""
HTML_END = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.3/js/bootstrap.bundle.min.js"></script>
</body>

</html>
"""
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
                                                                'smpSono': False}         


"""





