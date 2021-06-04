
import pandas as pd
import sys
import numpy as np
#import preprocess

#path = 'F:/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
#processpath = 'F:/20181110_gpsHealth/process/v3/'
path = '/media/wwang/easystore/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
processpath = '/media/wwang/easystore/20181110_gpsHealth/process/v3/'
path = 'F:/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
processpath = 'F:/20181110_gpsHealth/process/v3/'




#1. load data

#cities = ['wilmington','chattanooga','charleston','savanna','knoxville','newport_news']
citiesshort = ['wi','ct','cl','sa','kn','ne']
citiesshort_placeID = ['wi','sa','ne']
cities = ['wilmington','chattanooga','charleston','savanna','knoxville','newport_news']
cities_placeID = ['wilmington','savanna','newport_news']
cols4use_poi = ['advertiser_id', 'hour', 'date','athome', 'dist_home_avg', 'dist_home_max','dist_home_min','speed_avg', 'speed_max','familySize', 'athomeAvg', 'speed', 'together', 'togetherB_avg','togetherMember', 'placeID', 'nearestDist','blockFIPS']
cols4use_poi = ['advertiser_id', 'hour', 'date','athome', 'dist_home_avg', 'dist_home_max','dist_home_min','speed_avg', 'speed_max','familySize', 'athomeAvg', 'speed', 'together', 'togetherB_avg','togetherMember','blockFIPS']

cols4_treated_control = ['advertiser_id', 'hour', 'date','dist_home_avg', 'dist_home_max','dist_home_min','speed_avg', 'speed_max','familySize', 'athomeAvg','together','togetherB_avg','togetherMember', 'placeID', 'nearestDist','blockFIPS']
cols4_treated_partial_control = ['advertiser_id', 'hour', 'date','dist_home_avg', 'dist_home_max','dist_home_min','speed_avg', 'speed_max','familySize', 'athomeAvg','together','togetherB_avg','togetherMember','blockFIPS']
#in case that the data will be too big, now use the small version
cols4_treated_control = ['advertiser_id', 'hour', 'date','dist_home_avg','speed_avg', 'speed_max','familySize', 'athomeAvg','togetherB_avg', 'placeID', 'nearestDist','blockFIPS']
cols4_treated_partial_control = ['advertiser_id', 'hour', 'date','dist_home_avg','speed_avg', 'speed_max','familySize', 'athomeAvg','togetherB_avg','blockFIPS']


#construct full data - treated partial control
for i,city in enumerate(cities):
    print('working on: ',city)
    if city == 'wilmington':
        data = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge.csv'%city)
        data = data[cols4_treated_partial_control]
        data['city'] = [citiesshort[i]] * data.shape[0]
    else:
        temp = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge.csv'%city)
        temp = temp[cols4_treated_partial_control]
        temp['city'] = [citiesshort[i]] * temp.shape[0]
        data = pd.concat([data,temp],axis=0)

print(data.shape)
data.to_csv(processpath+'s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv',index=False)


del data, temp

#construct full data - treated partial control
for i,city in enumerate(cities_placeID):
    print('working on: ',city)
    if city == 'wilmington':
        data = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge.csv'%city)
        data = data[cols4_treated_control]
        data['city'] = [citiesshort_placeID[i]] * data.shape[0]
    else:
        temp = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge.csv'%city)
        temp = temp[cols4_treated_control]
        temp['city'] = [citiesshort_placeID[i]] * temp.shape[0]
        data = pd.concat([data,temp],axis=0)

print(data.shape)
data.to_csv(processpath+'s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.csv',index=False)

