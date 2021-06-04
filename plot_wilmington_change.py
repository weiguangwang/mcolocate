
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
projectpath = 'F:/20181110_gpsHealth/process/v3/'
censusblockpath = 'F:/gps_data/safegraph_data/OpenCensusData/openCensusData/'
censusblockpath = 'C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/data/censusBlock/'
resultpath = 'C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/'

# censusblockpath = '/media/wwang/work/temp/'
# resultpath = '/media/wwang/work/temp/'
# projectpath = 'C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/'
# processpath = 'C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/data/'

#1. load block data
def readBlockDemographic():
    selected=pd.read_csv(censusblockpath+'selected.csv')
    
    cols = ['blockFIPS','blockPopulation','income', 'incomeMedian', 'earning', 'wage', 'incomeSelf', 'incomeInterestRent', \
    'incomeSocialSecurity', 'incomePublicassistance', 'incomeRetirement', 'aggearning', 'aggwage', 'aggincomeSelf', \
    'aggincomeInterestRent', 'aggincomeSocialSecurity', 'aggincomePublicassistance', 'aggincomeRetirement', 'familyincome', \
    'aggfamilyincome', 'faimlyHasKid', 'familyMarriedHasKid', 'raceWhite', 'raceBlack', 'raceIndiaAmerican', 'raceAsian', \
    'raceHawaiia', 'raceOther', 'race2more', 'eduAll', 'eduMale', 'eduMaleNoschool', 'eduMaleHighschool', 'eduMaleBachelor', \
    'eduFemale', 'eduFemaleNoschool', 'eduFemaleHighschool', 'eduFemaleBachelor', 'bachelorFieldAll', \
    'bachelorFieldComputeMathStats', 'bachelorFieldBioAgricaltureEnvironment', 'bachelorFieldPhysical', \
    'bachelorFieldPsychology', 'bachelorFieldSocial', 'bachelorFieldEngineering', 'bachelorFieldBusiness', \
    'bachelorFieldEdu', 'bachelorFieldLitlanguage', 'bachelorFieldArthistory', 'bachelorFieldVisualPerforming', \
    'bachelorFieldCommunication', 'employment', 'fulltimeEmployment', 'maritalAll', 'maritalMale', 'maritalMaleNeverMarried', \
    'maritalMaleMarried', 'maritalMaleMarriedSpousePresent', 'maritalMaleMarriedSpouseAbsent', 'maritalMaleWidowed', \
    'maritalMaleD', 'maritaFemale', 'maritaFemaleNevermarried', 'maritaFemaleMarried', 'maritaFemaleMarriedSpousePresent', \
    'maritaFemaleMarriedSpouseAbsent', 'maritalFemaleWidowed', 'maritalFemaleD', 'housingunit', 'occupancyAll', \
    'occupancyOccupied', 'occupancyVacant', 'vacancyAll', 'vacancy4rent', 'vacancy4sale', 'vacancy4occasional', \
    'yearbuiltAll', 'yearbuilt2014late', 'yearbuilt2010', 'yearbuilt2000', 'yearbuilt1990', 'yearbuilt1980', 'yearbuilt1970', \
    'yearbuilt1960', 'yearbuilt1950', 'yearbuilt1940', 'yearbuilt1939early', 'yearbuiltMedian', 'yearbuiltMedianOccupied', \
    'yearbuiltMedianOccupiedOwner', 'yearbuiltMedianOccupiedRenter', 'vehiclenumberOccupied', 'vehiclenumberOccupiedOwner', \
    'vehiclenumberOccupiedRenter', 'plumbing', 'plumbingComplete', 'plumbingLack', 'kitchen', 'kitchenComplete', 'kitchenLack', \
    'contractrent', 'contractrentCash', 'contractrentNocash', 'contractrentLower', 'contractrentMedian', 'contractrentUpper', \
    'commuteTime', 'commuteCarTime', 'commuteCarpoolTime', 'commutePublicTime', 'commuteWalkTime', 'commuteAll', 'commuteCar', \
    'commutepublic', 'commuteTaxi', 'commuteMotor', 'commuteBike', 'commuteWalk', 'commuteHome', 'commuteTime0000', \
    'commuteTime0500', 'commuteTime0530', 'commuteTime0600', 'commuteTime0630', 'commuteTime0700', 'commuteTime0730', \
    'commuteTime0800', 'commuteTime0830', 'commuteTime0900', 'commuteTime1000', 'commuteTime1100', 'commuteTime1200', \
    'commuteTime1600', 'employmentCivilian', 'povertyAll', 'povertyBelow', 'povertyAbove']
    
    assert (selected['vacancyAll'] - selected['occupancyVacant']).max() == 0
    assert (selected['vacancyAll'] - selected['occupancyVacant']).min() == 0
    assert (selected['occupancyAll'] - selected['housingunit']).max() == 0
    assert (selected['occupancyAll'] - selected['housingunit']).min() == 0
    selected['familyMarriedHasKidRate'] = selected['familyMarriedHasKid']/selected['faimlyHasKid']
    selected['familyHasKidRate'] = selected['faimlyHasKid']/selected['blockPopulation']
    selected['raceAll']=selected['raceWhite']+selected['raceBlack']+selected['raceIndiaAmerican']+selected['raceAsian']+selected['raceHawaiia']+selected['raceOther']+selected['race2more']
    selected['raceWhiteRate'] = selected['raceWhite']/selected['raceAll']
    selected['raceBlackRate'] = selected['raceBlack']/selected['raceAll']
    selected['eduHighbelow']=selected['eduMaleNoschool']+selected['eduMaleHighschool']+selected['eduFemaleNoschool']+selected['eduFemaleHighschool']
    selected['eduHighbelowRate'] = selected['eduHighbelow']/selected['eduAll']
    selected['fulltimeEmploymentRate'] = selected['fulltimeEmployment']/selected['blockPopulation']
    selected['employmentCivilianRate'] = selected['employmentCivilian']/selected['blockPopulation']
    selected['employmentRate'] = selected['employment']/selected['blockPopulation']
    selected['marriedSpousePresentRate'] = (selected['maritalMaleMarriedSpousePresent']+selected['maritaFemaleMarriedSpousePresent'])/selected['maritalAll']
    selected['maritalDrate'] = (selected['maritalMaleD']+selected['maritalFemaleD'])/selected['maritalAll']
    selected['maritalWidowedRate'] = (selected['maritalMaleWidowed']+selected['maritalFemaleWidowed'])/selected['maritalAll']
    selected['vacancyRate'] = selected['vacancyAll']/selected['occupancyAll']
    selected['vacancy4occasionalRate'] = selected['vacancy4occasional']/selected['occupancyAll']
    selected['vacancy4rentRate'] = selected['vacancy4rent']/selected['occupancyAll']
    selected['vacancy4saleRate'] = selected['vacancy4sale']/selected['occupancyAll']
    selected['plumbingCompleteRate'] = selected['plumbingComplete']/selected['plumbing']
    selected['kitchenCompleteRate'] = selected['kitchenComplete']/selected['kitchen']
    selected['commuteCarRate'] = selected['commuteCar']/selected['commuteAll']
    selected['commutepublicRate'] = selected['commutepublic']/selected['commuteAll']
    selected['commuteWalkRate'] = selected['commuteWalk']/selected['commuteAll']
    selected['commuteHomeRate'] = selected['commuteHome']/selected['commuteAll']
    selected['povertyBelowRate'] = selected['povertyBelow']/selected['povertyAll']
    selected['vehiclenumberPerCapita'] = selected['vehiclenumberOccupied']/selected['blockPopulation']
    
    cols2use = ['blockFIPS', 'incomeMedian','familyMarriedHasKidRate','familyHasKidRate','raceBlackRate', 
    'eduHighbelowRate', 'fulltimeEmploymentRate', 'employmentRate','employmentCivilianRate','marriedSpousePresentRate', 'maritalDrate','maritalWidowedRate',
    'yearbuiltMedian', 'vehiclenumberPerCapita', 'plumbingCompleteRate', 'vacancyRate','vacancy4occasionalRate','vacancy4saleRate','vacancy4rentRate',
    'commuteTime','commutepublicRate','commuteWalkRate','commuteHomeRate','povertyBelowRate']
    
    selected = selected[cols2use]
    
    cols2plot = ['blockFIPS', 'incomeMedian','raceBlackRate','marriedSpousePresentRate','vacancyRate','vacancy4saleRate','vacancy4rentRate','commutepublicRate','commuteHomeRate']
    selected = selected[cols2plot]
    
    data=pd.read_excel(resultpath+'blockCohesion.xlsx')
    data = pd.merge(data,selected,how='left',left_on='blockfips',right_on='blockFIPS')
    return(data)




data = readBlockDemographic()
print(data.columns)



# import plotly.figure_factory as figure_factory  ##this package is only for county level data
# fig = ff.create_choropleth(fips=data['blockfips'].tolist(), scope=['NC'],values=data['incomeMedian'].tolist(), title='Wilmington Income', legend_title='Median Family Income')
# fig.layout.template = None
# fig.show()








import pandas as pd
import sys
import numpy as np
#import preprocess
import json
# from shapely.geometry import Polygon, Point
from matplotlib.patches import Polygon

import pickle
from matplotlib.collections import PatchCollection

#path = 'F:/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
#processpath = 'F:/20181110_gpsHealth/process/v3/'
path = '/media/wwang/easystore/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
processpath = '/media/wwang/easystore/20181110_gpsHealth/process/v3/'
path = 'F:/20181110_gpsHealth/data/aws_sync/6_cities_201807_201811/'
processpath = 'F:/20181110_gpsHealth/process/v3/'



def getNCpoly():
    # FIPS_state = [['37'],['47','13'],['45'],['13','45'],['47'],['51']]
    FIPS_state = [['37']]


    print('read polygon')
    with open('F:/20181110_gpsHealth/data/censusBlock/safegraph_census/cbg-004.geojson') as f:
        polygons = json.load(f)


    print('refine polygon')
    newPolygons = []
    for polygon in polygons['features']:
        if polygon['properties']['StateFIPS'] in FIPS_state[0]:
            # if polygon['properties']['CountyFIPS'] == FIPS_county[icity]:
            #     newPolygons.append(polygon)
            newPolygons.append(polygon)


    del polygons
    file = open("F:/20181110_gpsHealth/data/censusBlock/safegraph_census/NCblockPolygons.pickle","wb")
    pickle.dump(newPolygons,file)
    file.close()

    file = open("F:/20181110_gpsHealth/data/censusBlock/safegraph_census/NCblockPolygons.pickle",'rb')
    polygons = pickle.load(file)
    file.close()

###


file = open("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/data/censusBlock/NCblockPolygons.pickle",'rb')
polygons = pickle.load(file)
file.close()


from matplotlib import pyplot as plt
import matplotlib

def basemap():
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    lat_max = 36.885263
    lat_min = 33.748381
    lon_max = -74.309165
    lon_min = -79.718762


    patches = []
    istop = 0
    for polygon in polygons:
        istop += 1
        # print(istop)
        if istop > 10000000000:
            break
        else:
            shape = Polygon(polygon['geometry']['coordinates'][0][0],True)
            patches.append(shape)


    p = PatchCollection(patches, color='white', alpha=1,edgecolor='k', linewidths=1.5)
    
    ax.add_collection(p)
    ax.autoscale()

    ax.set_xlim(lon_min, lon_max)
    ax.set_ylim(lat_min, lat_max)

    plt.axis('off')
    plt.savefig(resultpath+'NCbase.png', bbox_inches='tight', pad_inches=0)
    
##    


def colorMap(colname,inverse=False):
    temp = data.loc[~data[colname].isna()]
    vmax = temp[colname].max()
    if inverse:
        temp[colname] = temp[colname].apply(lambda x:vmax-x)
        vmax = temp[colname].max()
        
    vmin = temp[colname].min() - (vmax-temp[colname].min())*.02
    vmin = min(0.0,vmin)
    currentDict = dict(zip(temp['blockfips'].tolist(),temp[colname].tolist()))
    
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    lat_max = 36.885263
    lat_min = 33.748381
    lon_max = -74.309165
    lon_min = -79.718762
    
    lat_max = 34.4
    lat_min = 34
    lon_max = -77.7
    lon_min = -78.1


    patches = []
    colorvalues = []
    istop = 0
    for polygon in polygons:
        istop += 1
        # print(istop)
        if istop > 10000000000:
            break
        else:
            currentFips = int(polygon['properties']['CensusBlockGroup'])
            if currentFips in temp['blockfips'].tolist():
                colorvalues.append(currentDict[currentFips]/vmax)
            else:
                colorvalues.append(vmin/vmax)
            
            shape = Polygon(polygon['geometry']['coordinates'][0][0],True)
            patches.append(shape)


    polygon = Polygon([(180,-90),(179.9,-90),(179.9,-89.9)], True)
    patches.append(polygon)
    colorvalues.append(vmax/vmax)
    polygon = Polygon([(180,-90),(179.9,-89.9),(180,-89.9)], True)
    patches.append(polygon)
    colorvalues.append(vmin/vmax)
    
    if colname in ['change']:
        p = PatchCollection(patches, cmap=matplotlib.cm.Reds,alpha=1,edgecolor='k', linewidths=1.5)
    elif colname in ['togetherb_avg_pre','togetherb_avg_post']:
        p = PatchCollection(patches, cmap=matplotlib.cm.Greens,alpha=1,edgecolor='k', linewidths=1.5)
    else:
        p = PatchCollection(patches, cmap=matplotlib.cm.Blues,alpha=1,edgecolor='k', linewidths=1.5)
    p.set_array(np.array(colorvalues))

    ax.add_collection(p)
    # ax.autoscale()

    handles = []
    numPoints = 5
    for point in range(numPoints):
        cvalue = vmin+(vmax-vmin)*(point+1)/numPoints
        if colname in ['change']:
            # handles.append(Polygon([(0,0),(10,0),(0,-10)],color=matplotlib.cm.Reds(cvalue/vmax),label='%.3f'%(vmax-cvalue)))
            handles.append(Polygon([(0,0),(10,0),(0,-10)],color=matplotlib.cm.Reds(cvalue/vmax),label='%.2f'%(cvalue)))
        elif colname in ['togetherb_avg_pre','togetherb_avg_post']:
            # handles.append(Polygon([(0,0),(10,0),(0,-10)],color=matplotlib.cm.Greens(cvalue/vmax),label='%.3f'%(vmax-cvalue)))
            handles.append(Polygon([(0,0),(10,0),(0,-10)],color=matplotlib.cm.Greens(cvalue/vmax),label='%.2f'%(cvalue)))
        else:
            # handles.append(Polygon([(0,0),(10,0),(0,-10)],color=matplotlib.cm.Blues(cvalue/vmax),label='%.3f'%(vmax-cvalue)))
            handles.append(Polygon([(0,0),(10,0),(0,-10)],color=matplotlib.cm.Blues(cvalue/vmax),label='%.2f'%(cvalue)))

    plt.legend(handles=handles)

    ax.set_xlim(lon_min, lon_max)
    ax.set_ylim(lat_min, lat_max)

    plt.axis('off')
    plt.savefig(resultpath+'NC_%s.png'%(colname), bbox_inches='tight', pad_inches=0)

    plt.close("all")
    plt.close(fig)
    fig.clear()
    del fig
    del ax

###


def colorMapCompare(colname,inverse=False):
    temp = data.loc[~data[colname].isna()]
    vmax = temp[colname].max()
    if inverse:
        temp[colname] = temp[colname].apply(lambda x:vmax-x)
        vmax = temp[colname].max()
        
    vmin = temp[colname].min() - (vmax-temp[colname].min())*.02
    vmin = min(0.0,vmin)
    currentDict = dict(zip(temp['blockfips'].tolist(),temp[colname].tolist()))
    
        
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    lat_max = 36.885263
    lat_min = 33.748381
    lon_max = -74.309165
    lon_min = -79.718762
    
    lat_max = 34.5
    lat_min = 33.9
    lon_max = -77.697675
    lon_min = -78.3


    patches = []
    colorvalues = []
    istop = 0
    for polygon in polygons:
        istop += 1
        # print(istop)
        if istop > 10000000000:
            break
        else:
            currentFips = int(polygon['properties']['CensusBlockGroup'])
            if currentFips in temp['blockfips'].tolist():
                colorvalues.append(currentDict[currentFips]/vmax)
            else:
                colorvalues.append(vmin/vmax)
            
            shape = Polygon(polygon['geometry']['coordinates'][0][0],True)
            patches.append(shape)


    polygon = Polygon([(180,-90),(179.9,-90),(179.9,-89.9)], True)
    patches.append(polygon)
    colorvalues.append(vmax/vmax)
    polygon = Polygon([(180,-90),(179.9,-89.9),(180,-89.9)], True)
    patches.append(polygon)
    colorvalues.append(vmin/vmax)
    
    p = PatchCollection(patches, cmap=matplotlib.cm.Blues,alpha=1,edgecolor='k', linewidths=0.1)
    p.set_array(np.array(colorvalues))

    ax.add_collection(p)
    # ax.autoscale()
    
    handles = []
    numPoints = 5
    for point in range(numPoints):
        cvalue = vmin+(vmax-vmin)*(point+1)/numPoints
        handles.append(Polygon([(0,0),(10,0),(0,-10)],color=matplotlib.cm.Blues(cvalue/vmax),label='%s %.1f'%(colname,cvalue)))
    
    
    
    temp = data.loc[~data['change'].isna()]
    vmax = temp['change'].max()        
    vmin = temp['change'].min() - (vmax-temp['change'].min())*.02
    vmin = min(0.0,vmin)
    currentDict = dict(zip(temp['blockfips'].tolist(),temp['change'].tolist()))
    
    istop = 0
    for polygon in polygons:
        istop += 1
        # print(istop)
        if istop > 10000000000:
            break
        else:
            currentFips = int(polygon['properties']['CensusBlockGroup'])
            if currentFips in temp['blockfips'].tolist():
                colorvalues.append(currentDict[currentFips]/vmax)
            else:
                colorvalues.append(vmin/vmax)
            
            shape = Polygon(polygon['geometry']['coordinates'][0][0],True)
            patches.append(shape)
            
    polygon = Polygon([(180,-90),(179.9,-90),(179.9,-89.9)], True)
    patches.append(polygon)
    colorvalues.append(vmax/vmax)
    polygon = Polygon([(180,-90),(179.9,-89.9),(180,-89.9)], True)
    patches.append(polygon)
    colorvalues.append(vmin/vmax)
    
    # p = PatchCollection(patches, cmap=matplotlib.cm.Reds,alpha=1,edgecolor='k', linewidths=0.1)
    # p.set_array(np.array(colorvalues))
    
    # ax.add_collection(p)
    # ax.autoscale()
    
    numPoints = 5
    for point in range(numPoints):
        cvalue = vmin+(vmax-vmin)*(point+1)/numPoints
        handles.append(Polygon([(0,0),(10,0),(0,-10)],color=matplotlib.cm.Reds(cvalue/vmax),label='%s %.1f%%'%('change',cvalue*100)))
    
    
    
    plt.legend(handles=handles)
    
    ax.set_xlim(lon_min, lon_max)
    ax.set_ylim(lat_min, lat_max)

    plt.axis('off')
    plt.savefig(resultpath+'NC_%s.png'%(colname), bbox_inches='tight', pad_inches=0)

    plt.close("all")
    plt.close(fig)
    fig.clear()
    del fig
    del ax




colorMap(colname= 'incomeMedian',inverse=False)
# colorMap(colname= 'raceBlackRate',inverse=False)
# colorMap(colname= 'marriedSpousePresentRate',inverse=True)
# colorMap(colname= 'vacancyRate',inverse=False)
# colorMap(colname= 'vacancy4saleRate',inverse=False)
# colorMap(colname= 'vacancy4rentRate',inverse=False)
# colorMap(colname= 'commutepublicRate',inverse=False)
# colorMap(colname= 'commuteHomeRate',inverse=True)

colorMap(colname= 'change',inverse=False)
# colorMap(colname= 'togetherb_avg_pre',inverse=False)
# colorMap(colname= 'togetherb_avg_post',inverse=False)


# colorMapCompare(colname= 'incomeMedian',inverse=True)
# colorMapCompare(colname= 'raceBlackRate',inverse=False)
# colorMapCompare(colname= 'marriedSpousePresentRate',inverse=True)
# colorMapCompare(colname= 'vacancyRate',inverse=False)
# colorMapCompare(colname= 'vacancy4saleRate',inverse=False)
# colorMapCompare(colname= 'vacancy4rentRate',inverse=False)
# colorMapCompare(colname= 'commutepublicRate',inverse=False)
# colorMapCompare(colname= 'commuteHomeRate',inverse=True)


