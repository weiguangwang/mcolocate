

import pandas as pd
import sys
#import preprocess
import pytz
import geopy.distance
mytz = pytz.timezone('America/New_York')

path = 'F:/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
processpath = 'F:/20181110_gpsHealth/process/v3/'
# poipath = 'C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/data/poi/'
poipath = 'F:/20181110_gpsHealth/data/poi/'
# path = '/media/wwang/easystore/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
# processpath = '/media/wwang/easystore/20181110_gpsHealth/process/v3/'

cities = ['wilmington','chattanooga','charleston','savanna','knoxville','newport_news']
for city in cities:
    print('working on: ',city)
    data = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID.csv'%city)
    del data['']
    
    data.to_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID.csv'%city,index=False)

