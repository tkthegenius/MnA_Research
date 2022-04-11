import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

data = yf.download(tickers='uber', period ='5d', invertal = '5m')
print(data)

df = pd.read_excel(r"C://Users/Kimtae4/Desktop/Working/MnA_Research/TargetData.xlsx")
print(df)
print(df.__len__)