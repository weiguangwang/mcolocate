




def homeLocation(data,loc_threshold = 50,midnightstart = 1, midnightend = 4, outputfile = None):
    # this function is to identify the home location for users
    # the logic: examine the location at midnight. if multiple loactions identified, examine the distance, 
    #        if short than loc_threshold (in meters) pick the center
    #        if longer than loc_threshold (in meters) pick the most frequent one (or center)
    #        
    # the midnightstart and midnightend are set as time that people should stay at home.
    from datetime import datetime
    from scipy.cluster.hierarchy import dendrogram, linkage  
    
    home = nightdata(data,midnightstart=midnightstart,midnightend=midnightend,outputfile=None,weekday='weekday')
    #home = home.drop_duplicates()
    home = home.sort_values('advertiser_id').reset_index(drop = True)
    
    uidlist = home['advertiser_id'].unique().tolist()
    newuids = []
    newlongs = []
    newlatis = []
    
    numUser = len(uidlist)
    counteri = 0

    for uid in uidlist:
        counteri +=1
        
        sys.stdout.write('working on %d / %d \r'%(counteri,numUser))
        temp = home.loc[home['advertiser_id']==uid]
        temp = temp.sort_values('location_at').reset_index(drop = True)
        longs = temp['longitude'].tolist()
        latis = temp['latitude'].tolist()
        
        if temp.shape[0] == 1:
            newuids.append(uid)
            newlongs.append(longs[0])
            newlatis.append(latis[0])
        else:
            '''#selfmade, too easy to consider the complex clustering
            places = []
            takenlist = []
            places_lon = []
            places_lat = []
            for i in range(temp.shape[0]):
                if i not in takenlist:
                    currentpoints = [i]
                    takenlist.append(i)
                    for j in range(temp.shape[0]):
                        if j not in takenlist:
                            if geopy.distance.vincenty((longs[i],latis[i]), (longs[j],latis[j])).m <= loc_threshold:
                                currentpoints.append(j)
                    places.append(len(currentpoints))
                    places_lon.append(np.mean(list( longs[v] for v in currentpoints)))
                    places_lat.append(np.mean(list( latis[v] for v in currentpoints)))
            
            if len(places) > 1:
                newuids.append(uid)
                newlongs.append(places_lon[places.index(max(places))])
                newlatis.append(places_lat[places.index(max(places))])
            elif len(places) == 0:
                pass
            else:
                newuids.append(uid)
                newlongs.append(places_lon[0])
                newlongs.append(places_lat[0])
            '''
            
            A = temp[['longitude','latitude']].as_matrix()
            linked = linkage(A, method = 'average',metric = geodist)
            #method could be: single, centroid, complete,average,weighted,median,ward
            #see here for more details: https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
            
            clusternumber = list(range(A.shape[0]))
            pointid = list(range(1,A.shape[0]+1))
            pointid = [[x] for x in pointid]
            count = [1] * A.shape[0]
            tempdict = dict(zip(clusternumber,pointid))
            tempdict_count = dict(zip(clusternumber,count))
            #print(linked,temp.shape,tempdict,tempdict_count)
            for i in range(linked.shape[0]):
                if linked[i][2] <= loc_threshold:
                    tempdict[int(linked.shape[0]+i+1)] = tempdict[int(linked[i][0])]+tempdict[int(linked[i][1])]
                    tempdict_count[int(linked.shape[0]+i+1)] = tempdict_count[int(linked[i][0])]+tempdict_count[int(linked[i][1])]
                    #del tempdict[linked[i][0]],tempdict[linked[i][1]]
            
            #print(tempdict_count,tempdict[max(tempdict_count, key=tempdict_count.get)])
            currentpoints = tempdict[max(tempdict_count, key=tempdict_count.get)]
            places_lon=np.mean(list( longs[v-1] for v in currentpoints))
            places_lat=np.mean(list( latis[v-1] for v in currentpoints))
            newuids.append(uid)
            newlongs.append(places_lon)
            newlatis.append(places_lat)
            
    print('')

    print('finished on %d / %d'%(counteri,numUser))
    temp = pd.DataFrame()
    temp['advertiser_id'] = newuids
    temp['longitude'] = newlongs
    temp['latitude'] = newlatis
    if outputfile:
        temp.to_pickle(outputfile)
    
    return(temp)





def nightdata(data,midnightstart=21,midnightend=5,outputfile=None,weekday = 'all'):
    from datetime import datetime
    from scipy.cluster.hierarchy import dendrogram, linkage
    
    datelist = data['starttime'].apply(lambda x:x.date()).unique().tolist()
    daylist = []
    yearlist = []
    monthlist = []
    hourstartlist = []
    hourendlist = []
    for onedate in datelist:
        daylist.append(onedate.day)
        yearlist.append(onedate.year)
        monthlist.append(onedate.month)
        hourstartlist.append(midnightstart)
        hourendlist.append(midnightend)
    '''
    daylist = [16,17,18]
    yearlist = [2018] * len(daylist)
    monthlist = [9] * len(daylist)
    hourstartlist = [midnightstart] * len(daylist)
    hourendlist = [midnightend] * len(daylist)
    '''
    startdatelist = []
    enddatelist = []
    for i in range(len(daylist)):
        if midnightstart > midnightend:
            startdatelist.append(datetime(yearlist[i],monthlist[i],daylist[i],hourstartlist[i],0,0,0,mytz))
            try:
                enddatelist.append(datetime(yearlist[i],monthlist[i],daylist[i]+1,hourendlist[i],0,0,0,mytz))
            except:
                enddatelist.append(datetime(yearlist[i],monthlist[i]+1,1,hourendlist[i],0,0,0,mytz))
        else:
            startdatelist.append(datetime(yearlist[i],monthlist[i],daylist[i],hourstartlist[i],0,0,0,mytz))
            enddatelist.append(datetime(yearlist[i],monthlist[i],daylist[i],hourendlist[i],0,0,0,mytz))
    
    if weekday == 'weekday':
        temp_startdatelist = []
        temp_enddatelist = []
        for i in range(len(startdatelist)):
            if enddatelist[i].weekday() in [2,3,4,5]:
                temp_startdatelist.append(startdatelist[i])
                temp_enddatelist.append(enddatelist[i])
        
        startdatelist = temp_startdatelist
        enddatelist = temp_enddatelist
        del temp_startdatelist, temp_enddatelist
    elif weekday == 'weekend':
        temp_startdatelist = []
        temp_enddatelist = []
        for i in range(len(startdatelist)):
            if enddatelist[i].weekday() in [1,6,7]:
                temp_startdatelist.append(startdatelist[i])
                temp_enddatelist.append(enddatelist[i])
        
        startdatelist = temp_startdatelist
        enddatelist = temp_enddatelist
        del temp_startdatelist, temp_enddatelist
    else:
        pass
    
    data = startendtime(data)
    for i in range(len(startdatelist)):
        print(startdatelist[i],enddatelist[i],enddatelist[i]-startdatelist[i])
        if i == 0:
            night = data.loc[(data['starttime']>=startdatelist[i]) & (data['endtime']<=enddatelist[i]) | (data['starttime']<=startdatelist[i]) & (data['endtime']>=enddatelist[i])]
            #print(night.shape)
        else:
            night=night.append(data.loc[(data['starttime']>=startdatelist[i]) & (data['endtime']<=enddatelist[i]) | (data['starttime']<=startdatelist[i]) & (data['endtime']>=enddatelist[i])])
            #print(night.shape)
    
    #night = night.drop_duplicates()
    if outputfile:
        night.to_pickle(outputfile)
    
    return(night)


