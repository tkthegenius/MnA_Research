
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
