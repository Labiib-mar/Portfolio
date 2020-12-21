import numpy as np
import pandas as pd
import re

data = pd.read_csv('delivery_orders_march.csv')
## columns [orderid, pick, 1st_deliver_attempt, 2nd_deliver_attempt, buyeraddress, selleraddress]


data['pick']= pd.to_datetime(data['pick'], unit='s')
data['1st_deliver_attempt']= pd.to_datetime(data['1st_deliver_attempt'], unit='s')
data['2nd_deliver_attempt']= pd.to_datetime(data['2nd_deliver_attempt'], unit='s')

data['pick'] = data['pick'].dt.date
data['1st_deliver_attempt'] = data['1st_deliver_attempt'].dt.date
data['2nd_deliver_attempt'] = data['2nd_deliver_attempt'].dt.date

print(data[['pick','1st_deliver_attempt','2nd_deliver_attempt']].head(5))

public_holidays = ['2020-03-08','2020-03-25','2020-03-30','2020-03-31']

dti= pd.bdate_range(start='03/01/2020', end='03/31/2020', freq = 'C',
                    holidays=public_holidays,
                    weekmask = 'Mon Tue Wed Thu Fri Sat')

##data['diff1'] = (data['1st_deliver_attempt']-data['pick']).dt.days.fillna(0)
##data['diff2'] = (data['2nd_deliver_attempt']-data['1st_deliver_attempt']).dt.days.fillna(0)
##
##print(data[['diff1','diff2']].head(5))

days =[]
for i in range((len(data))):
    dti= pd.bdate_range(start=data.iloc[i,1], end=data.iloc[i,2], freq = 'C',
                    holidays=public_holidays,
                    weekmask = 'Mon Tue Wed Thu Fri Sat')
    diff = len(dti)-1
    days.append(diff)

print(days)
    
##data['diff1'] = days
    


##xyz = data.loc[data['buyeraddress'].str.contains('metro manila', flags=re.I, regex=True), 'buyeraddress'] = 'Metro Manila'

##print(xyz)

data.loc[data['buyeraddress'].str.contains('metro manila', flags=re.I, regex=True), 'buyeraddress'] = 'Metro Manila'
data.loc[data['buyeraddress'].str.contains('luzon', flags=re.I, regex=True), 'buyeraddress'] = 'Luzon'
data.loc[data['buyeraddress'].str.contains('Visayas', flags=re.I, regex=True), 'buyeraddress'] = 'Visayas'
data.loc[data['buyeraddress'].str.contains('mindanao', flags=re.I, regex=True), 'buyeraddress'] = 'Mindanao'
print(data['buyeraddress'])

data.loc[data['selleraddress'].str.contains('metro manila', flags=re.I, regex=True), 'selleraddress'] = 'Metro Manila'
data.loc[data['selleraddress'].str.contains('luzon', flags=re.I, regex=True), 'selleraddress'] = 'Luzon'
data.loc[data['selleraddress'].str.contains('Visayas', flags=re.I, regex=True), 'selleraddress'] = 'Visayas'
data.loc[data['selleraddress'].str.contains('mindanao', flags=re.I, regex=True), 'selleraddress'] = 'Mindanao'
print(data['selleraddress'])
print(data['selleraddress'].describe())

data.loc
