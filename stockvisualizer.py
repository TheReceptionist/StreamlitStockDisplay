import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
@st.cache_data
def tickerListToDataFrame(tickers, timeframe):
    df_list = []
    df = pd.DataFrame()
    for ticker in tickers:
        data = yf.download(ticker, period=f'{timeframe}', group_by='column')
        data = data.get('Open').to_frame()
        data = data.rename(columns={'Open':f'{ticker}'})
        df_list.append(data)
    df = pd.concat(df_list, axis=1).fillna(0)
    return df
st.title('Display of stock prices of different portfolios')
timeframes = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
tf = st.selectbox('Select timeframe to display:', timeframes)
portfolios = {'Portfolio 1':[['GOOG', 'AAPL', 'UBER', 'LYFT', 'BA']],
             'Portfolio 2':[['A', 'OKTA', 'UHAL']],
             'Portfolio 3':[['NFLX', 'META', 'TSLA', 'DELL']]}
for p in portfolios.values():
    p.append(tickerListToDataFrame(p[0], tf))
portfol = st.selectbox('Select stock portfolio to display:', portfolios)
st.line_chart(portfolios[portfol][1])
st.bar_chart(portfolios[portfol][1])
date = next(iter(portfolios[portfol][1].index))
if tf != '1d':
    date = st.select_slider('Select date for pie chart', portfolios[portfol][1].index)
plt.pie(portfolios[portfol][1].loc[date], labels=portfolios[portfol][0], autopct = '%.0f%%')
st.pyplot(plt)
