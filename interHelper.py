import yfinance as yf 
import pandas as pd 


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

    
def addCompany(companyName, keysToGet):
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

def mainFunc(entries):
    