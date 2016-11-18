# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


#evens rows are call data
# odd rows are put data
data = pandas.read_csv('SPY-options-15-minute-calcs-20161101.csv')
    

QUOTE_DATE = "2016-11-01 16:00:00"
EXPIRATION = "2016-11-18"
T = 17/252
STEP = 5

print(data.size)
data = data[data['quote_datetime']==QUOTE_DATE]
print(data.size)
data = data[data['expiration']==EXPIRATION]
print(data.size)

S = (data.iloc[0]['underlying_bid'] + data.iloc[0]['underlying_ask'])/2
print("S: {0}".format(S))

calls = data[::2]
puts = data[1::2]

# filter for out-of-money options
calls = calls[calls['strike']>S]
puts = puts[puts['strike']<=S]

# filter for step size
calls = calls[calls['strike']%STEP==0]
puts = puts[puts['strike']%STEP==0]

# create option price from bid/ask spread
calls['option_price'] = (calls['bid'] + calls['ask'])/2
puts['option_price'] = (puts['bid'] +puts['ask'])/2

data = pandas.concat([calls,puts])

price = (2*STEP)/T * sum(data['option_price']/(data['strike']**2))

print("Variance Swap Price: {}".format(price))