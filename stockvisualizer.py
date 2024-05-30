import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# small function to get the ticker info and cache it
@st.cache_data
def getTickerInfo(ticker, timeframe):
    data = yf.download(ticker, period=f'{timeframe}', group_by='column')
    return data

# function to get the dataframe of stock prices from the list of tickers and chosen timeframe
def tickerListToDataFrame(tickers, timeframe):
    if not tickers:
        st.error("No tickers provided")
        st.stop()
    df_list = []
    df = pd.DataFrame()
    # Use finance api to populate dataframe with stock prices
    for ticker in tickers:
        try:
            data = getTickerInfo(ticker, timeframe)
        except KeyError as e:
            st.error('Invalid ticker')
            st.stop()
        #  print(f'getting data for the {global_var}\'th time')
        #  if not isinstance(data, pd.DataFrame):
        try:
            data = data.get('Open').to_frame()
        except AttributeError as e:
            st.error('Invalid format, remember to use commas')
            st.stop()
        # format into a usable table
        data = data.rename(columns={'Open':f'{ticker}'})
        df_list.append(data)
    df = pd.concat(df_list, axis=1).fillna(0)
    return df


st.title('Display of stock prices of different portfolios')
# container to display tabs later (streamlit displays widgets in order)
c = st.container(border=True)

timeframes = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

# store your portfolios so that they don't get overwritten on each page update
if 'portfolios' not in st.session_state:
    st.session_state['portfolios'] = {}
portfolios = st.session_state.portfolios

# function to associate portfolios with generated stock price dataframe
def storeportfolio(portfolio, tf):
    portfolio[1] = (tickerListToDataFrame(portfolio[0], tf))
    
# split the chart parameters and user-added portfolios into tabs
inserttab, selecttab, managetab = c.tabs(["Add portfolios", "Display Portfolios", "Manage Portfolios"])

with inserttab:
    #form to enter portfolio info
    form = st.form("my_form", border=False)
    form.subheader("Enter stocks to add to your portfolio")
    portname = form.text_input("Enter your portfolio name:")
    tickstr = form.text_input("Enter a comma-separated list of tickers:")
    # convert the string into a list of tickers
    ticklist = [x.strip().upper() for x in tickstr.split(',') if x != '']
    submit = form.form_submit_button()
    if submit:
        portfolios[f'{portname}'] = [ticklist, None]
        
with selecttab:
    tf = st.selectbox('Select timeframe to display:', timeframes)
    pf = st.selectbox('Select stock portfolio to display:', portfolios)   
    
with managetab:
    to_del = st.selectbox('Select stock portfolio to manage:', portfolios)
    col1, col2 = st.columns(2)
    removed = col1.button("Remove portfolio")
    removedAll = col2.button("Remove ALL portfolios", type="primary")
    if removed:
        if to_del in portfolios:
            del portfolios[to_del]
    if removedAll:
        portfolios.clear()
    
if portfolios != None and pf != None and removed != True and removedAll != True:
    storeportfolio(portfolios[pf], tf)
    st.line_chart(portfolios[pf][1])
    st.bar_chart(portfolios[pf][1])

    date = next(iter(portfolios[pf][1].index))
    if tf != '1d':
        date = st.select_slider('Select date for pie chart', portfolios[pf][1].index)
    plt.pie(portfolios[pf][1].loc[date], labels=portfolios[pf][0], autopct = '%.0f%%')
    st.pyplot(plt)
