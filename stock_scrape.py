import requests as rq
import json
import os
import pandas as pd
from requests.packages import urllib3

#disable annoying insecure requests message
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#get stock data to scrape
print('script works only with stocks no other instruments are supported')
stocks= pd.read_excel(r'D:\\1ahmed\\Python Scripts\\stock-scrapper-saxotrader\\DATA_2_EXTRACT.xlsx',sheet_name='Sheet1')

url = 'https://www.saxotrader.com/sim/openapi/chart/v3/charts?Mode=UpTo&FieldGroups=Data&count=1200&Horizon=60&Uic={0}&AssetType={1}&Time={2}T00%3A00%3A00.000Z'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','Authorization': 'BEARER '+input('PLease input auth:\n')}
date = input('Please input date as this format 2020&04&20 (yyyy&mm&dd)\n').replace('&','-')
#get data
for num in range(len(stocks)):

    stock_name = stocks['Stock'][num].replace('.','')
    stcok_num = str(stocks['uic'][num])
    stock_type = stocks['assest_type'][num]

    #handle data rq not getting 200
    rq_status = 409
    while rq_status == 409:
        data = rq.get(url.format(stcok_num,stock_type,date),headers=headers,verify=False)
        if data.status_code in [200,201,400,404]:
            break
       

    print("data status is "+str(data.status_code)+' Stock scrapped is '+stock_name+' num:'+stcok_num+' asset type '+stock_type)
    #process data into json
    try:
        data_dict = json.loads(data.text)
    except:
        pass
    #print(len(data_dict['Data']))
    #create dir for saving files
    save_dir = os.getcwd()+'\\data_collected'
    try:
        os.mkdir(os.getcwd()+'\\data_collected')
    except:
        pass
    #sometimes data is not available so it will raise key error while using data_dict
    try:
        if len(data_dict['Data']) != 0 :
            data_saved = pd.DataFrame(data_dict['Data'],columns=[i for i in data_dict['Data'][2].keys()])
            data_saved.to_excel(save_dir+'\\%s.xlsx'%stock_name)
        else:
            print('zero information needs subscription')
    except:
        pass
print("script finished")


