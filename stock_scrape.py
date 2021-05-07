import requests as rq
import json
import os
import pandas as pd
from requests.packages import urllib3
from random import random

#disable annoying insecure requests message
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#get stock data to scrape
print('script works only with stocks no other instruments are supported')
stocks= pd.read_excel(r'D:\\1ahmed\\Python Scripts\\stock-scrapper-saxotrader\\DATA_2_EXTRACT.xlsx',sheet_name='Sheet1')

url = 'https://www.saxotrader.com/sim/openapi/chart/v3/charts/subscriptions'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','Authorization': 'BEARER '+input('PLease input auth:\n'),'Content-Type': 'application/json'}
#date = input('Please input date as this format 2020&04&20 (yyyy&mm&dd)\n').replace('&','-')
rq_data ='{"Format":"application/x-protobuf","Arguments":{"Count":4000,"FieldGroups":["ChartInfo","Data","DisplayAndFormat"],"Horizon":60,"Uic":%s,"AssetType":%s},"RefreshRate":1000,"ContextId":%s,"ReferenceId":"68","KnownSchemas":["Chart-3.1.178+7cc0e4bccd"]}'
#get data
for num in range(len(stocks)):

    stock_name = stocks['Stock'][num].replace('.','')
    stcok_num = str(stocks['uic'][num])
    stock_type = stocks['assest_type'][num]
    randm = str(int(random()*100000))
    #handle data rq not getting 200
    
    def send_rq():
        rq_sent = rq.post(url,json=json.loads(rq_data % (stcok_num,'"'+stock_type+'"','"'+randm+'"')),headers=headers,verify=False)
        return rq_sent

    #my retry method (brutforce)
    try:
        data = send_rq()
    except:
        data = send_rq()

    print("data status is "+str(data.status_code)+' Stock scrapped is '+stock_name+' num:'+stcok_num+' asset type: '+stock_type)
    #process data into json
    data_dict = json.loads(data.text)
    #print(len(data_dict['Snapshot']['Data']))
    #create dir for saving files
    save_dir = os.getcwd()+'\\data_collected'
    try:
        os.mkdir(os.getcwd()+'\\data_collected')
    except:
        pass
    #sometimes data is not available so it will raise key error while using data_dict
    try:
        if len(data_dict['Snapshot']['Data']) != 0 :
            data_saved = pd.DataFrame(data_dict['Snapshot']['Data'],columns=[i for i in data_dict['Snapshot']['Data'][2].keys()])
            data_saved.to_excel(save_dir+'\\%s.xlsx'%stock_name)
        else:
            print('zero information needs subscription')
    except:
        pass
print("script finished")


