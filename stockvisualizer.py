import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from highcharts_core.chart import Chart as ct
import streamlit_highcharts as hct
import json
from ast import literal_eval


# small function to get the ticker info and cache it
@st.cache_data
def getTickerInfo(ticker, timeframe):
    data = yf.download(ticker, period=f'{timeframe}', group_by='column')
    return data

# function to get the dataframe of stock prices from the list of tickers and chosen timeframe
@st.cache_data
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
    form.subheader("Enter your portfolio")
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
SAMPLE={

    "title": {
        "text": 'U.S Solar Employment Growth by Job Category, 2010-2020'
    },

    "subtitle": {
        "text": 'Source: <a href="https://irecusa.org/programs/solar-jobs-census/" target="_blank">IREC</a>'
    },

    "yAxis": {
        "title": {
            "text": 'Number of Employees'
        }
    },

    "xAxis": {
        "accessibility": {
            "rangeDescription": 'Range: 2010 to 2020'
        }
    },

    "legend": {
        "layout": 'vertical',
        "align": 'right',
        "verticalAlign": 'middle'
    },

    "plotOptions": {
        "series": {
            "label": {
                "connectorAllowed": False
            },
            "pointStart": 2010
        }
    },

    "series": [{
        "name": 'Installation & Developers',
        "data": [43934, 48656, 65165, 81827, 112143, 142383,
            171533, 165174, 155157, 161454, 154610]
    }, {
        "name": 'Manufacturing',
        "data": [24916, 37941, 29742, 29851, 32490, 30282,
            38121, 36885, 33726, 34243, 31050]
    }, {
        "name": 'Sales & Distribution',
        "data": [11744, 30000, 16005, 19771, 20185, 24377,
            32147, 30912, 29243, 29213, 25663]
    }, {
        "name": 'Operations & Maintenance',
        "data": ["null", "null", "null", "null", "null", "null", "null",
            "null", 11164, 11218, 10077]
    }, {
        "name": 'Other',
        "data": [21908, 5548, 8105, 11248, 8989, 11816, 18274,
            17300, 13053, 11906, 10073]
    }],

    "responsive": {
        "rules": [{
            "condition": {
                "maxWidth": 500
            },
            "chartOptions": {
                "legend": {
                    "layout": 'horizontal',
                    "align": 'center',
                    "verticalAlign": 'bottom'
                }
            }
        }]
    }

}
hct.streamlit_highcharts(SAMPLE)
if portfolios != None and pf != None and removed != True and removedAll != True:
    storeportfolio(portfolios[pf], tf)
    port_data = portfolios[pf][1]
    port_label = portfolios[pf][0]
    ticker = yf.download("GOOG", period="1d", group_by='column')
    ticker = ticker.to_dict()
    ticker = pd.Series(ticker)
    x = ct.add_series(ticker)
    y = x.to_json()
    data = literal_eval(y.decode('utf8'))
    #  data["title"] = {"text":"Title lalalala"}
    st.write(data)
    hct.streamlit_highcharts(data)
    st.line_chart(port_data)
    st.bar_chart(port_data)

    date = next(iter(port_data.index))
    if tf != '1d':
        date = st.select_slider('Select date for pie chart', port_data.index)
    plt.pie(port_data.loc[date], labels=port_label, autopct = '%.0f%%')
    st.pyplot(plt)

