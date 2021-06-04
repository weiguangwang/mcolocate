
import pandas as pd
import sys
import numpy as np
import preprocess
import geopy

#path = 'F:/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
#processpath = 'F:/20181110_gpsHealth/process/v3/'
# path = '/media/wwang/easystore/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
# processpath = '/media/wwang/easystore/20181110_gpsHealth/process/v3/'
path = 'F:/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
processpath = 'F:/20181110_gpsHealth/process/v3/'



def userIDconver(family):
    temp=pd.read_excel(processpath+'iddict_v1.xlsx')
    templist = temp['advertiser_id'].to_list()
    values = temp['advertiser_id_convertedid'].to_list()
    iddict = dict(zip(templist,values))
    ids = family['advertiser_id'].to_list()
    newids = []
    for id in ids:
        tempid = []
        for iid in id:
            if iid in (templist):
                tempid.append(iddict[iid])
        newids.append(tempid)
    familySize = []
    family['advertiser_id'] = newids
    familySize = [len(x) for x in newids]
    family['familySize'] = familySize
    family = family.loc[~family['familySize'].isin([0,1])]
    return(family)

###

def createFamilyDict(family):
    fam_uidslist = family['advertiser_id'].tolist()
    
    #all_fam_uids = [item for sublist in fam_uidslist for item in sublist]
    all_fam_uids = []
    for fam_uids in fam_uidslist:
        if len(fam_uids) > 1:
            all_fam_uids += fam_uids

    valuestemp = []
    keystemp = []
    for i,fam_uids in enumerate(fam_uidslist):
        if len(fam_uids) > 1:
            for fam_uid in fam_uids:
                keystemp.append(fam_uid)
                valuestemp.append(i)
    
    famIDdict = dict(zip(keystemp,valuestemp))
    all_fam_uids = list(set(all_fam_uids))
    return(famIDdict,all_fam_uids,fam_uidslist)

###

def outWithFamilyHourly(data,family,loc_threshold = 50, time_match_threshold=6*60,outputfile=None,do_togetherMember=False):
    # this function is to identify the places that a person go out to with at least one family member
    # the input data is abouthome data (using longstay data), which is the output of homestaylenN()
    # family is the output of samehome()
    # loc_threshold is max distance that we think the two person are at the same location when do matching. Better to set it as the error of this gps data
    # time_match_threshold is the max time that we think the two person are at somewhere the same time. Better to set it as the delayed capture.
    
    famIDdict,all_fam_uids,fam_uidslist = createFamilyDict(family)
    
    outTogethor = []
    if do_togetherMember:
        togetherMember = []
    totalNum = data.shape[0]
    advertiser_ids = data['advertiser_id'].tolist()
    longs = data['longitude'].tolist()
    latis = data['latitude'].tolist()
    dates = data['date'].tolist()
    hours = data['hour'].tolist()
    
    totalNum = len(advertiser_ids)
    numPersons = 0
    print('')
    focalID = 99999999
    for i in range(totalNum):
        sys.stdout.write('\r==%s/%s,%s===\r'%(i+1,totalNum,numPersons))
        numPersons = 0
        if advertiser_ids[i] not in all_fam_uids:
            print('error 2',advertiser_ids[i])    #a user is not in the family list, which should not happen because we have excluded users whose family size is smaller than 2.
            outTogethor.append(0)
            if do_togetherMember:
                togetherMember.append([])
        else:
            if focalID == advertiser_ids[i]:
                focalDate = dates[i]
                focalHour = hours[i]
                temp = rest_data.loc[(rest_data['date']==focalDate) & (rest_data['hour']==focalHour)]
                focalLong = longs[i]
                focalLati = latis[i]
                templongs = temp['longitude'].tolist()
                templatis = temp['latitude'].tolist()
                tempusers = temp['advertiser_id'].tolist()
                togetherMembers = []
                for j in range(temp.shape[0]):
                    if tempusers[j] not in togetherMembers:
                        # if geopy.distance.vincenty((templongs[j],templatis[j]), (focalLong,focalLati)).m < loc_threshold:
                        if geopy.distance.great_circle((templongs[j],templatis[j]), (focalLong,focalLati)).m < loc_threshold:
                            numPersons += 1
                            togetherMembers.append(tempusers[j])
                outTogethor.append(numPersons)
                if do_togetherMember:
                    togetherMember.append(togetherMembers)
            else:
                focalID = advertiser_ids[i]
                famID = famIDdict[focalID]
                rest_uids = [x for x in fam_uidslist[famID] if x!= focalID]
                rest_data = data.loc[data['advertiser_id'].isin(rest_uids)]
                
                focalDate = dates[i]
                focalHour = hours[i]
                temp = rest_data.loc[(rest_data['date']==focalDate) & (rest_data['hour']==focalHour)]
                focalLong = longs[i]
                focalLati = latis[i]
                templongs = temp['longitude'].tolist()
                templatis = temp['latitude'].tolist()
                tempusers = temp['advertiser_id'].tolist()
                togetherMembers = []
                for j in range(temp.shape[0]):
                    if tempusers[j] not in togetherMembers:
                        # if geopy.distance.vincenty((templongs[j],templatis[j]), (focalLong,focalLati)).m < loc_threshold:
                        if geopy.distance.great_circle((templongs[j],templatis[j]), (focalLong,focalLati)).m < loc_threshold:
                            numPersons += 1
                            togetherMembers.append(tempusers[j])
                outTogethor.append(numPersons)
                if do_togetherMember:
                    togetherMember.append(togetherMembers)
    
    data['togethor'] = outTogethor
    if do_togetherMember:
        data['togetherMember'] = togetherMember
    if outputfile:
        data.to_pickle(outputfile)
    
    del data['longitude']
    del data['latitude']
    del data['date']
    del data['hour']
    return(data)




#cities = ['wilmington','chattanooga','charleston','savanna','knoxville','newport_news']
cities = ['wilmington','chattanooga']
# cities = ['charleston','savanna','knoxville','newport_news']
for city in cities:
    print('working on: ',city)
    data = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly.csv'%city)
    data = data[['advertiser_id','longitude','latitude','date','hour']]
    file = '%s_07_11_both_valid10'%city    
    family = pd.read_pickle(processpath+'%s_family.pickle'%file)
    family = userIDconver(family)
    family = family.reset_index(drop=True)
    
    if city != 'charleston':
        data = outWithFamilyHourly(data,family,loc_threshold = 50, time_match_threshold=6*60,outputfile=None,do_togetherMember=True)
    else:
        data = outWithFamilyHourly(data,family,loc_threshold = 50, time_match_threshold=6*60,outputfile=None,do_togetherMember=False)
        
    print('')
    print('saving')
    #data = outdf
    data.to_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_togetherOnly.csv'%city,index=False)
    del data



print('step 1 finished')


for city in cities:
    print('working on: ',city)
    data = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_togetherOnly.csv'%city)
    together = data['togethor'].tolist()
    if city != 'charleston':
        togetherMember = data['togetherMember'].tolist()
    del data
    data = pd.read_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly.csv'%city)
    data['togethor'] = together
    del together
    if city != 'charleston':
        data['togetherMember'] = togetherMember
        del togetherMember
    print('')
    print('saving')
    #data = outdf
    data.to_csv(processpath+'%s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together.csv'%city,index=False)
    del data
    



# cities = ['wilmington','chattanooga','charleston','savanna','knoxville','newport_news']
# cities_placeID = ['wilmington','savanna','newport_news']
# cols4use_poi = ['advertiser_id', 'longitude', 'latitude', 'hour', 'date','athome', 'dist_home', 'familySize', 'speed', 'together', 'togetherMember', 'placeID', 'nearestDist']
# cols4use = ['advertiser_id', 'longitude', 'latitude', 'hour', 'date','athome', 'dist_home', 'familySize', 'speed','together', 'togetherMember']

