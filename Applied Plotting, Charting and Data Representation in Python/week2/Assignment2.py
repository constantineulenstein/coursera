
# coding: utf-8

# # Assignment 2
#
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
#
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
#
# Each row in the assignment datafile corresponds to a single observation.
#
# The following variables are provided to you:
#
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
#
# For this assignment, you must:
#
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
#
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[98]:

import matplotlib.pyplot as plt
#import mplleaflet
import pandas as pd
import numpy as np

# def leaflet_plot_stations(binsize, hashid):

#     df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

#     station_locations_by_hash = df[df['hash'] == hashid]

#     lons = station_locations_by_hash['LONGITUDE'].tolist()
#     lats = station_locations_by_hash['LATITUDE'].tolist()

#     plt.figure(figsize=(8,8))

#     plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

#     return mplleaflet.display()

# leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[ ]:

df = pd.read_csv('fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df['Data_Value'] = df['Data_Value']/10


# In[111]:

#filter max and mins and drop 2015 data & group by data and max()
df_max=df[(df['Element']=='TMAX') & (df['Date']<='2014-12-31')].groupby(['Date'], sort=True)['Data_Value'].max().reset_index()
df_min=df[(df['Element']=='TMIN') & (df['Date']<='2014-12-31')].groupby(['Date'], sort=True)['Data_Value'].min().reset_index()

#convert to timestamps
df_max['Date'] = list(map(pd.to_datetime, df_max['Date']))
df_min['Date'] = list(map(pd.to_datetime, df_min['Date']))

#drop year
df_max['Date'] = df_max['Date'].apply(lambda x: x.strftime('%m-%d'))
df_min['Date'] = df_min['Date'].apply(lambda x: x.strftime('%m-%d'))

#groupby date and max()
df_max=df_max.groupby(['Date'], sort=True)['Data_Value'].max().reset_index()
df_min=df_min.groupby(['Date'], sort=True)['Data_Value'].min().reset_index()

#reset_index for cleaning
df_max = df_max[df_max['Date']!='02-29'].reset_index()
df_min = df_min[df_min['Date']!='02-29'].reset_index()


#plotting
fig = plt.figure()
plt.plot(df_max['Data_Value'],'-', df_min['Data_Value'], '-', alpha=0.7)
#fill difference between max and min
plt.gca().fill_between(range(len(df_max['Data_Value'])),
                       df_min['Data_Value'], df_max['Data_Value'],
                       facecolor='grey',
                       alpha=0.15,
                       label='_nolegend_')

#scatter data for 2015
df_max_2015 = df[(df['Element']=='TMAX') & (df['Date']>'2014-12-31')].groupby(['Date'], sort=True)['Data_Value'].max().reset_index()
df_min_2015 = df[(df['Element']=='TMIN') & (df['Date']>'2014-12-31')].groupby(['Date'], sort=True)['Data_Value'].max().reset_index()

#condition if higher or lower than max and min
df_max_2015 = df_max_2015[df_max_2015['Data_Value']>df_max['Data_Value']]
df_min_2015 = df_min_2015[df_min_2015['Data_Value']<df_min['Data_Value']]

#include scattered data
plt.scatter(df_max_2015.index, df_max_2015['Data_Value'], s=5, c='red')
plt.scatter(df_min_2015.index, df_min_2015['Data_Value'], s=5, c='blue')

#x-axis display by months
month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
DayOfMonth=[1,32,60,91,121,152,182,213,244,274,305,335]
plt.xticks(DayOfMonth)
plt.xticks(DayOfMonth,month,alpha=0.8)

#other beautifying
plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')
plt.ylabel('Temperature in \N{DEGREE SIGN}C')
plt.title('Record highs and lows for 2005-2014 near Ann Arbor\n (including days in 2015 that broke this record high or low)')
plt.legend(['High (05-14)', 'Low (05-14)', 'Breaking high (15)', 'Breaking low (15)'])

# remove the frame of the chart
for spine in plt.gca().spines.values():
    spine.set_visible(False)

plt.show()




