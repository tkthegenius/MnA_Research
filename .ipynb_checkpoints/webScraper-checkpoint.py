#author Taekyu Kim 
#version 1.0 

import pandas as pd
import time
from datetime import datetime
from webScraperHelper import addCompany

fileIn = 'Scrape Test'
pathIn = 'playground/Lib/original/'
pathOut = 'playground/Lib/out/'
sleepCount = 0

codeToGet = pd.DataFrame(pd.read_excel(pathIn + fileIn + '.xlsx', 'Sheet1'))

codes = codeToGet[codeToGet['Code'].notnull()]

keysToGet = ['fullTimeEmployees', 'city', 'state', 'country','profitMargins', 'grossMargins', 'operatingMargins','grossProfits','totalRevenue']

df = pd.DataFrame(columns = keysToGet)

for x in codes['Code']:
    sleepCount += 5
    
    df = pd.concat([df, addCompany(x,keysToGet)])
    
    print('Taking a nap to reset...')
    time.sleep(5)
    print("I have slept for ", sleepCount, " seconds... ready to retry")

print("=======================================Done!============================================")
now = datetime.now()
dateNTime = now.strftime("%d%m%Y_%H%M%S_")

fileName = fileIn + "_" + dateNTime + "dataList.xlsx"
df.to_excel(pathOut + fileName)