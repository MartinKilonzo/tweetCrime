import numpy as np
import pandas as pd

from UTMtoLatLong import UTMtoLatLong

df = pd.read_csv('./crimeData/crime_csv_all_years.csv')

latitude = []
longitude = []

for X, Y in zip(df['X'], df['Y']):
    lat, lng = UTMtoLatLong(10, X, Y)
    latitude.append(lat)
    longitude.append(lng)


df['LATITUDE'] = latitude
df['LONGITUDE'] = longitude
df = df.dropna()


df

bondaryBox = ((-123.22474,49.198177),(-123.023068,49.317294))





'https://indico.io/'
'https://www.quandl.com/browse?idx=database-browser_commodity-data_energy_spot-prices'
'http://www.svennerberg.com/2008/11/bounding-box-in-google-maps/'
'http://boundingbox.klokantech.com/'
