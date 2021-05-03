import requests as rq
import json

url = 'https://www.saxotrader.com/sim/openapi/chart/v3/charts?Mode=UpTo&FieldGroups=Data&count=1200&Horizon=60&Uic={0}&AssetType={1}&Time={2}T00%3A00%3A00.000Z'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','Authorization': 'BEARER '+input('PLease input auth:\n')}

data = rq.get(url.format('30440','Stock',input('Please input date as this format 2020&04&20 (yyyy&mm&dd)\n').replace('&','-')),headers=headers,verify=False)

print("data status is "+str(data.status_code))

data_dict = json.loads(data.text)
print(len(data_dict['Data']))

