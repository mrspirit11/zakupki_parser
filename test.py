import requests, json
from pprint import pprint as pp

purch_numb = '32009805853', '32009744334'
 
url = f'https://zakupki.gov.ru/api/mobile/proxy/917/223/purchase/public/purchase/info/common-info.html?regNumber={purch_numb[1]}'

json_data = json.loads(requests.get(url, headers={'User-Agent':'1'}).text)['data']

# customer = {
#   'inn':json_data['noticeInfo']['customerInn'],
#   'name':json_data['noticeInfo']['customerName']
# }


pp(json_data)
