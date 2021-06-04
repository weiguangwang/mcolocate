
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


cities = ['wilmington','chattanooga','charleston','savanna','knoxville','newport_news']
cities_placeID = ['wilmington','savanna','newport_news']
cols4use_poi = ['advertiser_id', 'longitude', 'latitude', 'hour', 'date','athome', 'dist_home', 'familySize', 'speed', 'together', 'togetherMember', 'placeID', 'nearestDist','blockFIPS']
cols4use = ['advertiser_id', 'longitude', 'latitude', 'hour', 'date','athome', 'dist_home', 'familySize', 'speed','together', 'togetherMember','blockFIPS']

for city in cities:
    print('working on: ',city)
    data = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID.csv'%city)
    # del data['longitude']
    # del data['latitude']
    data = data.loc[data['blockFIPS']!= 100]
    
    if 'together' not in data.columns.tolist():
        data['together'] = data['togethor']
        del data['togethor']
    
    data['togetherB'] = (data['together']>0).astype(int)
    temp=pd.DataFrame()
    temp['together'] = data.groupby(['advertiser_id','hour','date'])['together'].mean()
    del data['together']
    temp['athomeAvg'] = data.groupby(['advertiser_id','hour','date'])['athome'].mean()
    del data['athome']
    temp['togetherB_avg'] = data.groupby(['advertiser_id','hour','date'])['togetherB'].mean()
    del data['togetherB']
    temp['dist_home_avg'] = data.groupby(['advertiser_id','hour','date'])['dist_home'].mean()
    temp['dist_home_max'] = data.groupby(['advertiser_id','hour','date'])['dist_home'].max()
    temp['dist_home_min'] = data.groupby(['advertiser_id','hour','date'])['dist_home'].min()
    del data['dist_home']
    
    speeds = data['speed'].tolist()
    maxspeeds = []
    avgspeeds = []
    for speed in speeds:
        if speed=='[]':
            speed = []
        else:
            speed = speed.replace('[','').replace(']','').replace(' ','').replace(',,',',').split(',')
        if len(speed) != 0:
            speed = [float(x) for x in speed]
            speed = [x for x in speed if x != 0]
        if len(speed) == 0:
            maxspeeds.append(0)
            avgspeeds.append(0)
        elif len(speed) == 1:
            maxspeeds.append(speed[0])
            avgspeeds.append(speed[0])
        elif len(speed) > 1:
            maxspeeds.append(np.max(speed))
            avgspeeds.append(np.mean(speed))
    
    del data['speed'],speeds
    data['maxspeed']=maxspeeds
    data['avgspeed'] = avgspeeds
    del maxspeeds,avgspeeds
    data['maxspeed'].replace(0, np.NaN)
    data['avgspeed'].replace(0, np.NaN)
    temp['speed_avg'] = data.groupby(['advertiser_id','hour','date'])['avgspeed'].mean()
    temp['speed_max'] = data.groupby(['advertiser_id','hour','date'])['maxspeed'].max()
    del data['maxspeed'],data['avgspeed']
    
    # data['athome'] = data.groupby(['advertiser_id','hour','date'])['athome'].apply(lambda x: ','.join(x)).reset_index()
    # data['dist_home'] = data.groupby(['advertiser_id','hour','date'])['dist_home'].apply(lambda x: ','.join(x)).reset_index()
    # data['speed'] = data.groupby(['advertiser_id','hour','date'])['speed'].apply(lambda x: ','.join(x)).reset_index()
    # data['together'] = data.groupby(['advertiser_id','hour','date'])['together'].apply(lambda x: ','.join(x)).reset_index()
    if city != 'charleston':
        data['togetherMember'] = data.groupby(['advertiser_id','hour','date'])['togetherMember'].apply(lambda x: ','.join(x)).reset_index()
    if city in cities_placeID:
        data['placeID'] = data.groupby(['advertiser_id','hour','date'])['placeID'].apply(lambda x: ','.join(x)).reset_index()
        # data['nearestDist'] = data.groupby(['advertiser_id','hour','date'])['nearestDist'].apply(lambda x: ','.join(x)).reset_index()
        # temp['nearestDist_min'] = data.groupby(['advertiser_id','hour','date'])['nearestDist'].min().reset_index()
        
    data = data.drop_duplicates(['advertiser_id','hour','date'])
    data = pd.merge(data, temp,  how='left', left_on=['advertiser_id','hour','date'], right_on = ['advertiser_id','hour','date'])
    
    print('')
    print('saving')
    #data = outdf
    data.to_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge.csv'%city,index=False)
    del data




