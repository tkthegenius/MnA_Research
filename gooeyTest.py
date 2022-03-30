from __future__ import print_function
import os
import json
import time
import datetime
import pandas as pd
import yfinance as yf
from gooey import Gooey, GooeyParser

sleepCount = 0

@Gooey(program_name="Company Financial Data Collector", menu=[{'name': 'File', 'items': [{
    'type': 'AboutDialog',
    'menuTitle': 'About',
    'name': 'Financial Data Collector',
    'description': 'Accelerate your data research process so you can move on from the grunt work',
    'version': '1.0.0',
    'copyright': '2021 TK',
    'developer': 'AAC Market Strategy e-mobility Taekyu Kim',
}]}])
def parse_args():
    """ Use GooeyParser to build up the arguments we will use in our script
    Save the arguments in a default json file so that we can retrieve them
    every time we run the script.
    """
    stored_args = {}
    # get the script name without the extension & use it to build up
    # the json filename
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    args_file = "{}-args.json".format(script_name)
    # Read in the prior arguments as a dictionary
    if os.path.isfile(args_file):
        with open(args_file) as data_file:
            stored_args = json.load(data_file)
    parser = GooeyParser(description='Company Financial Data Collector')
    parser.add_argument('data_directory',
                        action='store',
                        default=stored_args.get('data_directory'),
                        widget='FileChooser',
                        help="Source directory that contains Excel files")
    parser.add_argument('output_directory',
                        action='store',
                        widget='DirChooser',
                        default=stored_args.get('output_directory'),
                        help="Output directory to save collected data file")
    parser.add_argument('columnHeads', 
                        action='store',
                        default=stored_args.get('columnHeads'),
                        widget='Listbox',
                        help="Parameters you would like to retrieve",
                        nargs="+",
                        choices=[
                            'fullTimeEmployees','city','state','country','website','ebitdaMargins','profitMargins','grossMargins','operatingCashflow','revenueGrowth','operatingMargins','ebitda','grossProfits','freeCashflow','targetMedianPrice','currentPrice','earningsGrowth','currentRatio','returnOnAssets','targetMeanPrice','returnOnEquity','totalCash','totalDebt','totalRevenue','financialCurrency','market','totalAssets','bookValue'
                        ]
                        )
    args = parser.parse_args()
    # Store the values of the arguments so we have them next time we run
    with open(args_file, 'w') as data_file:
        # Using vars(args) returns the data as a dictionary
        json.dump(vars(args), data_file)
    return args

def combine_files(src_directory):
    """ Read in source excel file and create data frame to retrieve target companies 
    """

    all_Data = pd.DataFrame(pd.read_excel(src_directory))
    specific_Data = all_Data[all_Data['Code'].notnull()]

    return specific_Data

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

def addCompany(companyName):
    newDat = {}
    shortDict = {}
    comp = yf.Ticker(companyName)
    for key, value in comp.info.items():
        newDat[key] = value
    for keys in conf.columnHeads:
        if keys in newDat.keys():
            shortDict[keys] = newDat[keys]
        else:
            shortDict[keys] = 'N/A'
    try:
        shortDict['CAGR'] = calculateCagr(comp)
    except RuntimeError:
        print("An Error has occurred, couldn't calculate CAGR")
    return pd.DataFrame(shortDict, index = [companyName]) 


def save_results(nameDf, collected_data, output):
    """ save created financial data dataframe into selected folder for output 
    """
    now = datetime.datetime.now()
    dateNTime = now.strftime("%d%m%Y_%H%M%S")
    collected_data = collected_data.reset_index()
    out_Data = pd.concat([nameDf, collected_data], axis = 1)
    out_Data = out_Data.rename({'index':'Code'}, axis = 1)
    out_Data.set_index('Name', inplace=True)
    out_Data.profitMargins *= 100
    out_Data.grossMargins *= 100
    out_Data.operatingMargins *= 100
    #out_Data = out_Data.rename({'fullTimeEmployees':'Employees','city':'City','state':'State','country':'Country','profitMargins':'Profit Margins','grossMargins':'Gross Margins','operatingMargins':'Operating Margins', 'grossProfits':'Gross Profits', 'totalRevenue':'Total Revenue'}, axis = 1)
    outputFileDir = output + "/" + dateNTime + "_financials.xlsx"
    out_Data.to_excel(outputFileDir)


if __name__ == '__main__':
    conf = parse_args()
    print("Reading file")
    sales_df = combine_files(conf.data_directory)
    codes = sales_df['Code']
    names = sales_df['Name']
    nameDf = pd.DataFrame(names).reset_index()
    nameDf = nameDf.loc[:,['Name']]
    outputFile = pd.DataFrame(columns = conf.columnHeads)
    print("Retrieving and saving requested data")
    for code in codes:
        sleepCount += 5
        try:
            outputFile = pd.concat([outputFile, addCompany(code)])
        except (RuntimeError):
            print("server is not responding")
            break
        print("Taking a power nap...")
        time.sleep(5)
        print("I have slept for ", sleepCount, " seconds... ready to retry")
    save_results(nameDf, outputFile, conf.output_directory)
    print("Done")