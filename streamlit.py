import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
time_intervals = 30
st.title('Display of stock prices of different portfolios')
portfolios = {'Portfolio 1':['Google', 'Apple', 'Versa', 'Uber', 'Lyft', 'Boeing'],
             'Portfolio 2':['Netflix', 'Twitter', 'Facebook'],
             'Portfolio 3':['Netflix', 'Twitter', 'Facebook', 'Yahoo']}

portfol = st.selectbox('Select stock portfolio to display:', portfolios)
#randomly generate stock prices
values = np.random.randint(100,1000,(time_intervals,len(portfolios[portfol])))
stocks_chart = pd.DataFrame(data=values, columns=portfolios[portfol])
st.line_chart(stocks_chart)
st.bar_chart(stocks_chart)
st.title('Pie chart showing % of total stock price on a given date')
date = st.slider('Select date for pie chart', min_value = 0, max_value = time_intervals-1 )
plt.pie(values[date], labels=portfolios[portfol], autopct = '%.0f%%')
st.pyplot(plt)
