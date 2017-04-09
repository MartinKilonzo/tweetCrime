%matplotlib inline


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from UTMtoLatLong import UTMtoLatLong

df = pd.read_csv('./crimeData/VanCrimeData2017.csv')

latitude = []
longitude = []

for X, Y in zip(df['X'], df['Y']):
    lat, lng = UTMtoLatLong(10, X, Y)
    latitude.append(lat)
    longitude.append(lng)


df['LATITUDE'] = latitude
df['LONGITUDE'] = longitude
# df = df.dropna()

df

subset = df.loc[df.YEAR > 2016]

subset

sns.barplot(x=subset['TYPE'].value_counts(), y=subset['TYPE'].value_counts().index)

plt.savefig('crimes.png', bbox_inches='tight', orientation='landscape', dpi=400)


bondaryBox = ((-123.22474,49.198177),(-123.023068,49.317294))





# 'https://indico.io/'
# 'https://www.quandl.com/browse?idx=database-browser_commodity-data_energy_spot-prices'
# 'http://www.svennerberg.com/2008/11/bounding-box-in-google-maps/'
# 'http://boundingbox.klokantech.com/'
