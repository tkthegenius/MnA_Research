import yfinance as yf 
import pandas as pd 
from cagrHelper import calculateCagr

def addCompany(companyName, keysToGet):
    newDat = {}
    comp = yf.Ticker(companyName)
    for key, value in comp.info.items():
        newDat[key] = value
    shortDict = {}
    for keys in keysToGet:
        if keys in newDat.keys():
            shortDict[keys] = newDat[keys]
        else:
            shortDict[keys] = 'N/A'
    try:
        shortDict['CAGR'] = calculateCagr(comp)
    except RuntimeError:
        print('error has occured')
    return pd.DataFrame(shortDict, index = [companyName])