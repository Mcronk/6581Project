# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas
import calendar
import datetime
import zipfile
import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D

#Open all zip files


def is_nth_weekday(nth, daynum, today):
    return calendar.Calendar(daynum).monthdatescalendar(
        today.year, 
        today.month
    )[nth][0]


#create csv

x = os.getcwd()
folderList = [a for a in os.listdir(x) if os.path.isdir(a) and a[0]!='.']

print (folderList)

for folder in folderList:
#Reference for all zip files containing csv data
	fileList = os.listdir(folder)
	fileList = [os.path.join(folder,f) for f in fileList]
	for f in fileList:
		zip_ref = zipfile.ZipFile(f, 'r')
		zip_ref.extractall(folder)
		zip_ref.close()


		fileName = f[0:-4]+".csv"
		print (fileName)
		#evens rows are call data
		# odd rows are put data

		data = pandas.read_csv(fileName)

		fileDate = datetime.date(int(f[-12:-8]),int(f[-8:-6]),int(f[-6:-4]))
		
		QUOTE_DATE = fileDate.strftime('%Y-%m-%d')	
		QUOTE_DATE = QUOTE_DATE + " 16:00:00"
		EXPIRATION_DATETIME = is_nth_weekday(3,4,fileDate)# 3 is thurday, 4 is friday, 5 is saturday
		EXPIRATION = str(EXPIRATION_DATETIME)



		difference = (EXPIRATION_DATETIME - fileDate).days
		T = difference/252.0
		STEP = 5


		# print(data.shape[0])
		data = data[data['quote_datetime']==QUOTE_DATE]
		# print(data.shape[0])
		data = data[data['expiration']==EXPIRATION]


		# print(data.shape[0])
		# print(data.head(5))

		print "\n"
		S = (data.iloc[0]['underlying_bid'] + data.iloc[0]['underlying_ask'])/2
		# print("S: {0}".format(S))

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

		#Add info to combined csv in parent directory :D
		#delete expanded file
		os.remove(fileName)
