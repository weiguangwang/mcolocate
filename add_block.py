
import pandas as pd
import sys
import numpy as np
#import preprocess
import json
from shapely.geometry import Polygon, Point

#path = 'F:/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
#processpath = 'F:/20181110_gpsHealth/process/v3/'
path = '/media/wwang/easystore/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
processpath = '/media/wwang/easystore/20181110_gpsHealth/process/v3/'
path = 'F:/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
processpath = 'F:/20181110_gpsHealth/process/v3/'


# cities = ['wilmington','chattanooga','charleston','savanna','knoxville','newport_news']
cities = ['newport_news']
cities_placeID = ['wilmington','savanna','newport_news']
cols4use_poi = ['advertiser_id', 'longitude', 'latitude', 'hour', 'date','athome', 'dist_home', 'familySize', 'speed', 'together', 'togetherMember', 'placeID', 'nearestDist']
cols4use = ['advertiser_id', 'longitude', 'latitude', 'hour', 'date','athome', 'dist_home', 'familySize', 'speed','together', 'togetherMember']

# FIPS_state = [['37'],['47','13'],['45'],['13','45'],['47'],['51']]
FIPS_state = [['51']]
FIPS_county = ['129','140',]

temp = pd.read_excel(processpath+'iddict_v1.xlsx')  # datedict_v1.xlsx and iddict_v1.xlsx are both generated by id_date_convert_v1.py
iddict = dict(zip(temp['advertiser_id'],temp['advertiser_id_convertedid']))
del temp

for icity,city in enumerate(cities):
    print('working on: ',city)
    file = '%s_07_11_both_valid10'%city
    
    try:
        family = pd.read_pickle(processpath+'%s_family_blcokFIPS.pickle'%file)
    except:
        # family blockFIPS not obtained
        family = pd.read_pickle(processpath+'%s_family.pickle'%file)
        
        latitudes = family['latitude'].tolist()
        longitudes = family['longitude'].tolist()
        
        print('read polygon')
        with open('F:/20181110_gpsHealth/data/censusBlock/safegraph_census/cbg-004.geojson') as f:
            polygons = json.load(f)
        
        print('refine polygon')
        newPolygons = []
        for polygon in polygons['features']:
            if polygon['properties']['StateFIPS'] in FIPS_state[icity]:
                # if polygon['properties']['CountyFIPS'] == FIPS_county[icity]:
                #     newPolygons.append(polygon)
                newPolygons.append(polygon)
        
        del polygon
        
        print('family block')
        blocks = []
        for ifamily in range(family.shape[0]):
            currentBlock = []
            p = Point(longitudes[ifamily],latitudes[ifamily])
            for polygon in newPolygons:
                poly=Polygon(polygon['geometry']['coordinates'][0][0])
                if poly.contains(p):
                    currentBlock.append(polygon['properties']['CensusBlockGroup'])
            
            if len(currentBlock)>1:
                print('error',currentBlock)
            else:
                if len(currentBlock)==0:
                    print('no block')
                    blocks.append(100)
                else:
                    blocks.append(currentBlock[0])
        
        family['blockFIPS'] = blocks
        family.to_pickle(processpath+'%s_family_blcokFIPS.pickle'%file)
        del newPolygons,blocks,latitudes,longitudes
    
    
    fam_uidslist = family['advertiser_id'].tolist()
    blocks = family['blockFIPS'].tolist()
    userID = []
    blockFIPS = []
    for ifamily in range(family.shape[0]):
        for user in fam_uidslist[ifamily]:
            userID.append(iddict[user])
            blockFIPS.append(blocks[ifamily])
    
    blockDict = dict(zip(userID,blockFIPS))
    del family,blocks,fam_uidslist,userID,blockFIPS
    
    
    print('block FIPS to data')
    data = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together.csv'%city)
    del data['longitude']
    del data['latitude']
    advertiser_ids = data['advertiser_id'].tolist()
    blockFIPSs = []
    for advertiser_id in advertiser_ids:
        blockFIPSs.append(blockDict[advertiser_id])
    
    data['blockFIPS']=blockFIPSs
    del advertiser_ids, blockFIPSs,blockDict
    
    print('')
    print('saving')
    #data = outdf
    data.to_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID.csv'%city,index=False)
    del data
