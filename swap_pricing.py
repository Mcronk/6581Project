# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas
import csv
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
#results = open("results.csv", 'w')
fieldnames = ['quote_date','expiration_date','var_swap_price']

resultsFile = 'results_{}.csv'.format(datetime.date.today())
if os.path.exists(resultsFile):
	os.remove(resultsFile) 
with open(resultsFile,'a') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()


# run in /development/execution/options-15-minute-calcs/
x = os.getcwd()
folderList = [a for a in os.listdir(x) if os.path.isdir(a) and a[0]!='.']

print (folderList)

for folder in folderList:

	folderList2 = [os.path.join(folder,a) for a in os.listdir(folder) 
						if os.path.isdir(os.path.join(folder, a))]
						
	for folder2 in folderList2:
	#Reference for all zip files containing csv data
		fileList = os.listdir(folder2)
		fileList = [os.path.join(folder2, f) for f in fileList]
		for f in fileList:
			zip_ref = zipfile.ZipFile(f, 'r')
			zip_ref.extractall(folder2)
			zip_ref.close()


			fileName = os.path.splitext(f)[0]+".csv"
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
			with open(resultsFile,'a') as csvfile:
				csvWriter = csv.DictWriter(csvfile,fieldnames=fieldnames)
				csvWriter.writerow({'quote_date': QUOTE_DATE, 'expiration_date':EXPIRATION, 'var_swap_price':price})


