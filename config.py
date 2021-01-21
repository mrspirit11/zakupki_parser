# coding= UTF8

HOST = 'https://zakupki.gov.ru/api/mobile/proxy/917/'

SEARCH_URL = HOST + 'epz/order/extendedsearch/results.html'

PURCHASE_URLS = {'223': HOST + '223/purchase/public/purchase/info/common-info.html',
                 '44': HOST + 'epz/order/notice/{}/view/common-info.html',
                 '615': HOST + 'epz/order/notice/{}/view/common-info.html'}

PROTOCOL_URLS = {'44': HOST + 'epz/order/notice/{}/view/supplier-results.html',
                 '615': HOST + 'epz/order/notice/{}/view/supplier-results.html'}

HEADERS = {'User-Agent': 'okhttp/3.12.1'}

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
    <link rel="stylesheet" href="assets/css/styles.css">
</head>

<body>
    <div class="container" style="margin: 0px;margin-top: 16px;margin-bottom: 0px;">
"""
HTML_TEXT = """<p style="margin-bottom: 1px;line-height: 15px;text-align: center;font-size: 16px;"><a href="{href}">{titleName}</a><br></p>
        <p style="font-size: 14px;margin: 0px;margin-bottom: 10px;margin-top: 0px;text-align: center;"><strong>{number}</strong></p>
        <p style="font-size: 14px;margin: 0px;margin-bottom: 3px;margin-top: 0px;">{provider}, {method}</p>
        <div class="table-responsive" style="margin: 0px;text-align: left;">
            <table class="table">
                <thead>
                    <tr></tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="font-size: 14px;padding: 2px;width: 113px;">Обновлено:</td>
                        <td style="font-size: 14px;padding: 2px;">{updateDate}</td>
                    </tr>
                    <tr style="padding: 2px;">
                        <td style="font-size: 14px;padding: 2px;width: 150px;">Этап закупки:&nbsp;</td>
                        <td style="font-size: 14px;padding: 2px;"><strong>{stagetStr}</strong></td>
                    </tr>
                    <tr style="padding: 2px;">
                        <td style="font-size: 14px;padding: 2px;width: 185px;">Подача заявки:</td>
                        <td style="font-size: 14px;padding: 2px;">{createDate}<br>{tillDate}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="table-responsive" style="padding: 2px;">
            <table class="table">
                <thead style="padding: 2px;">
                    <tr style="padding: 2px;"></tr>
                </thead>
                <tbody style="padding: 2px;">
                    <tr style="padding: 2px;"></tr>
                    <tr style="padding: 2px;">
                        <td style="padding: 2px;font-size: 14px;width: 190px;">Начальная цена контракта:</td>
                        <td style="padding: 2px;font-size: 14px;"><strong>{price:,} &#8381</strong></td>
                    </tr>
                    <tr style="padding: 2px;font-size: 12px;">
                        <td style="padding: 2px;font-size: 14px;width: 236px;">Обеспечение заявки:</td>
                        <td style="padding: 2px;font-size: 14px;"><strong>{ensuringPurchase:,} &#8381</strong></td>
                    </tr>
                    <tr style="padding: 2px;font-size: 12px;">
                        <td style="padding: 2px;font-size: 14px;">Обеспечение контракта:</td>
                        <td style="padding: 2px;font-size: 14px;"><strong>{ensuringPerformanceContrac:,} &#8381; {contractGrntShare}%</strong></td>
                    </tr>
                    <tr style="padding: 2px;font-size: 12px;">
                        <td style="padding: 2px;font-size: 14px;">Обеспечение гарантийных:</td>
                        <td style="padding: 2px;font-size: 14px;"><strong>{warrantyObligationsSize:,} &#8381</strong></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p style="font-size: 14px;">{organization}</p>"""
HTML_WIN = """<p style="margin-bottom: 2px;font-size: 14px;">Победитель - 1</p>
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr></tr>
                </thead>
                <tbody>
                    <tr style="font-size: 13px;padding: 0px;">
                        <td style="font-size: 14px;padding: 0px;width: 242px;">{1 - Победитель}</td>
                        <td style="font-size: 14px;padding: 0px;"><strong>{1 - Победитель - предл:,} &#8381</strong></td>
                    </tr>
                    <tr></tr>
                </tbody>
            </table>
        </div>
        """
HTML_COMM = '<p style="margin-bottom: 16px;font-size: 14px;"><em>{коммент}</em></p>'
HTML_COMPL = """<div class="alert alert-success" role="alert" style="background: #ffe0e3;font-size: 14px;"><span style="color: rgb(0,0,0);">{complaints}</span></div>"""
HTML_END = """</div>
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





