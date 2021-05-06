import requests
import os
import redis
import re
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from django.http import *
from zipfile import ZipFile
from io import BytesIO
from datetime import *
from django.conf import settings
from django.shortcuts import render,redirect
from dateutil.parser import parse as parsedate
from current_date_today import custom_today_date
from django.http import response
from textwrap3 import wrap
from celery import shared_task





'''import zlib
import glob'''

#need to change for production values giving by redis heroku
redis_instance = redis.StrictRedis(host='localhost',port=6379, db=0)

def get_link():
    urls = []
    reqs = requests.get('https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx',headers={
      'User-Agent': 'Mozilla/5.0'
    })
    data = reqs.text
    soup = BeautifulSoup(data,'html.parser')
    for link in soup.find_all('a',href=re.compile("Equity")):
        if link.get('href') is not None and link.get('href') not in urls:
            urls.append(link.get('href'))
    if urls!=[]:
        return urls[0]
    else:
        return None


def check_file_last_update_date(file_name):
    curr = wrap(str(file_name.split('.')[0][2:]),2)
    m = datetime(int(str(custom_today_date().split('-')[0][0:2]) + str(curr[2])), int(curr[1]), int(curr[0]))
    print(custom_today_date())
    print(m.strftime('%Y-%m-%d'))
    return m.strftime('%Y-%m-%d') == custom_today_date()


#Extract the zip file and save the CSV File into the folder if not present in folder
@shared_task(name="download_equity")
def download_equity():
    print('runing')
    print(get_link())
    if get_link() is not None:
        print('working')
        req = requests.get(get_link(),headers={'User-Agent': 'Mozilla/5.0'},stream=True)
        z = ZipFile(BytesIO(req.content))
        #check for csv file latest update date : - if true extract it else False
        #another method we can  do to get url header last modified date but somtimes it will return 
        #NONE resulting avoding breaking code issue
        print(check_file_last_update_date(z.namelist()[0]))
        if check_file_last_update_date(z.namelist()[0]):
            req = requests.get(get_link(),headers={'User-Agent': 'Mozilla/5.0'},stream=True)
            #if new file is extract the data directly other than saving it because heroku don't support static files,
            # to save it check below commented check
            z = ZipFile(BytesIO(req.content))
            df = pd.read_csv(z.open(z.namelist()[0]),usecols=['SC_CODE','SC_NAME','OPEN','HIGH','LOW','CLOSE'])
            keys = ['SC_CODE','SC_NAME','OPEN','HIGH','LOW','CLOSE']
            for key in keys:
                redis_instance.set(key,str(df[key].tolist()))   #temp commented should be removed comment 
            #As heroku don't serve static file so we are not saving the file first
            #if you want to first save the extract file in folder run this check it will save the file into the save  path 
            #but if file already exist it will not extract the file 
            
            #BASE_DIR = Path(__file__).resolve().parent.parent
            #save_path = os.path.join(BASE_DIR,'equity_downloads')
            #if os.path.exists(save_path + r'/' + z.namelist()[0]):
            #    return False
            #else:
            #    z.extractall(save_path)
            z.close()
            return f"done"
        else:
            return f"up-to-date"

    else:
       return None

def Scheduling_func():
    pass



def download_csv(request):
    if get_link() is not None:
        items = {}
        req = requests.get(get_link(),headers={'User-Agent': 'Mozilla/5.0'},stream=True)
        z = ZipFile(BytesIO(req.content))
        df = pd.read_csv(z.open(z.namelist()[0]),usecols=['SC_CODE','SC_NAME','OPEN','HIGH','LOW','CLOSE'])
        items["SC_CODE"] = df["SC_CODE"]
        items["SC_NAME"] = df["SC_NAME"]
        items["OPEN"] = df["OPEN"]
        items["HIGH"] = df["HIGH"]
        items["LOW"] = df["LOW"]
        items["CLOSE"] = df["CLOSE"]
        df = pd.DataFrame(items, columns= ['SC_CODE','SC_NAME','OPEN','HIGH','LOW','CLOSE'])
        return HttpResponse(df.to_csv(),content_type='text/csv',headers={"Content-disposition":"attachment; filename=Equity.csv"})
    else:
        pass