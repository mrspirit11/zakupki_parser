# import requests, json
# from pprint import pprint as pp

# purch_numb = '32009805853', '32009736982'
 
# url_223 = f'https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/common-info.html?regNumber={purch_numb[1]}'

# url_44 = 'https://zakupki.gov.ru/api/mobile/proxy/917/epz/order/notice/ok504/view/common-info.html?regNumber=0372100017820000041'

# json_data_223 = json.loads(requests.get(url_223, headers={'User-Agent':'1'}).text)['data']
# json_data = json.loads(requests.get(url_44, headers={'User-Agent':'1'}).text)['data']['dto']
# customer = {
#   'inn':json_data['noticeInfo']['customerInn'],
#   'name':json_data['noticeInfo']['customerName']
# }

# pp(json_data_223)


from datetime import datetime, timedelta



print(get_date_from())