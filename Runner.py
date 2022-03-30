#!/usr/bin/env python
# coding: utf-8
# author: Taekyu Kim 

# In[135]:

import pandas as pd
import yfinance as yf
from datetime import datetime
import time
sleepCount = 0


# In[136]:


fileIn = '220304_TAM'
pathIn = 'playground/Lib/original/'
pathOut = 'playground/Lib/out/'
keysToGet = ['fullTimeEmployees', 'city', 'state', 'country','profitMargins', 'grossMargins', 'operatingMargins','grossProfits','totalRevenue']


# In[137]:


def calculateCagr(ticker):
    sheet = ticker.financials
    try:
        revRow = sheet.loc[['Total Revenue'],:]
    except (RuntimeError):
        raise RuntimeError("there is no 'total revenue' information available.")
    revRow = revRow.loc[:,revRow.any()]
    CAGR = (revRow.iloc[:,0][0]/revRow.iloc[:,-1][0])**(1/(int(revRow.columns[0].strftime('%Y'))-int(revRow.columns[len(revRow.columns)-1].strftime('%Y'))))-1
    CAGR *= 100
    return CAGR


# In[138]:


def addCompany(companyName):
    newDat = {}
    shortDict = {}
    comp = yf.Ticker(companyName)
    for key, value in comp.info.items():
        newDat[key] = value
    for keys in keysToGet:
        if keys in newDat.keys():
            shortDict[keys] = newDat[keys]
        else:
            shortDict[keys] = 'N/A'
    try:
        shortDict['CAGR'] = calculateCagr(comp)
    except RuntimeError:
        print("An Error has occurred, couldn't calculate CAGR")
    return pd.DataFrame(shortDict, index = [companyName]) 


# In[139]:


codeToGet = pd.DataFrame(pd.read_excel(pathIn + fileIn + ".xlsx",sheet_name = 'Market insights'))
codeToGet = codeToGet.iloc[1:,:]
codes = codeToGet[codeToGet['Code'].notnull()]
names = codes['Name']
codes = codes['Code']


# In[140]:


now = datetime.now()
dateNTime = now.strftime("%d%m%Y_%H%M%S")


# In[141]:


df = pd.DataFrame(columns = keysToGet)


# In[151]:


for code in codes:
    sleepCount += 5
    try:
        df = pd.concat([df, addCompany(code)])
    except (RuntimeError):
        print("server is not responding")
        break
    print("Taking a power nap...")
    time.sleep(5)
    print("I have slept for ", sleepCount, " seconds... ready to retry")


# In[150]:
nameDf = pd.DataFrame(names).reset_index()
nameDf = nameDf.loc[:,['Name']]
df = df.reset_index()
df = pd.concat([nameDf, df],axis = 1)
df = df.rename({'index':'Code'}, axis = 1)
df.profitMargins *= 100
df.grossMargins *= 100
df.operatingMargins *= 100
df = df.rename({'fullTimeEmployees':'Employees','city':'City','state':'State','country':'Country','profitMargins':'Profit Margins','grossMargins':'Gross Margins','operatingMargins':'Operating Margins', 'grossProfits':'Gross Profits', 'totalRevenue':'Total Revenue'}, axis = 1)

print("===================================================================Done!===========================================================================")

fileName = fileIn + "_" + dateNTime + "dataList.xlsx"
df.to_excel(pathOut + fileName)