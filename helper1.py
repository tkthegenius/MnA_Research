import yfinance as yf 

name = ['TTDKY']
name2 = ['5401.T','4004.T','6501.T','015860.KS','PH','53L','3407.T']

data = {}

def addCompInfo(companyName):
    comp = yf.Ticker(companyName)
    for key, value in comp.info.items():
        data[key] = value
    print(data)
    if 'city' in data.keys():
        print([["HQ :",data['city'], data['country']],["Employees: ", data['fullTimeEmployees']], data['longBusinessSummary']])
    elif 'state' in data:
        print([["HQ :",data['city'], data['state'], data['country']],["Employees: ", data['fullTimeEmployees']], data['longBusinessSummary']])
    elif 'country' in data:
        print([["HQ :", data['country']],["Employees: ", data['fullTimeEmployees']], data['longBusinessSummary']])
    else:
        print([["Employees: ", data['fullTimeEmployees']], data['longBusinessSummary']])


for sname in name:
    addCompInfo(sname)