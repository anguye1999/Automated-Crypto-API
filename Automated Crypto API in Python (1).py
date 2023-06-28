#!/usr/bin/env python
# coding: utf-8

# # Automated Crypto API in Python

# In[2]:


from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'15',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'a23a1ae5-e4cb-47df-8741-c38bd142b541',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


# In[3]:


type(data)


# In[4]:


# import pandas in order to increase the amount of columns showing 

import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[5]:


# this line of code normalize the data which means to make it look pretty in a dataframe

df = pd.json_normalize(data['data'])

df['timestamp'] = pd.to_datetime('now')

df


# In[6]:


# define a function to call api to run 

def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'15',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'a23a1ae5-e4cb-47df-8741-c38bd142b541',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
    
    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now')
    df
#     df_append = pd.DataFrame(df2)
#     df = pd.concat([df,df_append])
    # df = df.append(df2) alternative option to run
    
    
    # creates a csv file in the file path 
    if not os.path.isfile(r'/Users/andynguyen/Documents/Python Scripts/API.csv'):
        df.to_csv(r'/Users/andynguyen/Documents/Python Scripts/API.csv', header = 'column_names')
    else:
        df.to_csv(r'/Users/andynguyen/Documents/Python Scripts/API.csv', mode = 'a', header = False)
        
        


# In[7]:


import os
from datetime import datetime 
from time import sleep

for i in range(333): #iterate the api with range of 333 which is the daily amount for this api
    api_runner()
    print('API Runner completed successfully')
    sleep(60) #sleep for 1 minute
exit()


# In[10]:


# Reads the csv file that was made

df72 = pd.read_csv(r'/Users/andynguyen/Documents/Python Scripts/API.csv')
df72


# In[11]:


df


# In[14]:


# change the scientific notation within the data

pd.set_option('display.float_format', lambda x: '%.5f' % x) 


# In[15]:


df


# In[16]:


# displays the mean of off the crypto by time
#however, the format of this chart is not good visually

df3 = df.groupby('name', sort = False)[['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d','quote.USD.percent_change_60d', 'quote.USD.percent_change_90d']].mean()
df3


# In[17]:


# create another variable df4 to stack the data fro each crypto

df4 = df3.stack()
df4


# In[18]:


type(df4)


# In[19]:


# change the variable df4 to a dataframe type from series

df5 = df4.to_frame(name = 'values')
df5


# In[20]:


df5.count()


# In[21]:


# change the index
index = pd.Index(range(90))

df6 = df5.reset_index()

df6


# In[22]:


df7 = df6.rename(columns = {'level_1': 'percent_change'})
df7


# In[23]:


df7['percent_change'] = df7['percent_change'].replace(['quote.USD.percent_change_1h','quote.USD.percent_change_24h','quote.USD.percent_change_7d','quote.USD.percent_change_30d','quote.USD.percent_change_60d','quote.USD.percent_change_90d'], ['1h','24h','7d','30d','60d','90d'])

df7


# In[24]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[35]:


sns.catplot(x = 'percent_change', y = 'values', hue = 'name', data = df7, kind = 'point')

