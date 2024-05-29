import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
#  stock = pd.DataFrame(np.array([[1,2,3], [4,5,6]]), columns=['a', 'b', 'c'], index=[-1, 0])
#  portfolio = pd.DataFrame(np.random.randn(10,5), columns = ("Stock %d" % i for i in range(5)))
#  for i in portfolios:
    #  portfolios[i]
#  stock = pd.read_csv('/home/holden/Downloads/Apple.csv')
#  stock
#  st.line_chart(stock, x='Date', y='Open')
time_intervals = 30
st.title('Display of stock prices of different portfolios')
portfolios = {'Portfolio 1':['Google', 'Apple', 'Versa', 'Uber', 'Lyft', 'Boeing'],
             'Portfolio 2':['Netflix', 'Twitter', 'Facebook'],
             'Portfolio 3':['Netflix', 'Twitter', 'Facebook', 'Yahoo']}
x = st.selectbox('Select stock portfolio to display:', portfolios)
values = np.random.randint(100,1000,(time_intervals,len(portfolios[x])))
stocks_chart = pd.DataFrame(data=values, columns=portfolios[x])
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(stocks_chart)
st.bar_chart(stocks_chart)
st.title('Pie chart showing % of total stock price on a given date')
y = st.slider('Select date for pie chart', min_value = 0, max_value = time_intervals-1 )
plt.pie(values[y], labels=portfolios[x], autopct = '%.0f%%')
st.pyplot(plt)
