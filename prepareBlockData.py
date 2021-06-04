
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

# projectpath = 'C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/'
censusblockpath = 'F:/gps_data/safegraph_data/OpenCensusData/openCensusData/'

#0. read blockIDs
# temp = pd.read_csv(projectpath+'data/s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.csv',usecols=['blockFIPS'])
temp = pd.read_csv(processpath+'s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.csv',usecols=['blockFIPS'])
blockIDs = temp['blockFIPS'].unique().tolist()
del temp


#1. read selected columns
# selected = pd.read_excel(projectpath+'data/censusBlock/cbg_field_descriptions_selecting.xlsx')
selected = pd.read_excel(censusblockpath+'cbg_field_descriptions_selecting.xlsx')
selected=selected.loc[selected['colname'].notnull()]

tableIDs = selected['table_id'].tolist()
colNames = selected['colname'].tolist()
tableIDs.append('census_block_group')
colNames.append('blockFIPS')
iddict = dict(zip(tableIDs,colNames))
del colNames

tables = [x[:3] for x in tableIDs]
tables = list(set(tables))
del selected

firstcol = True
for table in tables:
    print(table)
    selectedCol = ['census_block_group']
    try:
        
        for itable,tableid in enumerate(tableIDs):
            if tableid[1:3] == table[1:]:
                selectedCol.append(tableid)
        # temp = pd.read_csv(projectpath+'data/censusBlock/openCensusData/data/cbg_b%s.csv'%table[1:],usecols=selectedCol)
        temp = pd.read_csv(censusblockpath+'data/cbg_b%s.csv'%table[1:],usecols=selectedCol)
        temp = temp.loc[temp['census_block_group'].isin(blockIDs)]
        if firstcol:
            selected = temp
            firstcol = False
        else:
            # selected=pd.concat([selected,temp],axis=1)
            selected=pd.merge(selected,temp,left_on='census_block_group',right_on='census_block_group',how='left')
    except Exception as e:
        print(e)
        print('pass',table)


for table in tables:
    print(table)
    selectedCol = ['census_block_group']
    try:
        
        for itable,tableid in enumerate(tableIDs):
            if tableid[1:3] == table[1:]:
                selectedCol.append(tableid)
        # temp = pd.read_csv(projectpath+'data/censusBlock/openCensusData/data/cbg_b%s.csv'%table[1:],usecols=selectedCol)
        temp = pd.read_csv(censusblockpath+'data/cbg_c%s.csv'%table[1:],usecols=selectedCol)
        temp = temp.loc[temp['census_block_group'].isin(blockIDs)]
        # selected=pd.concat([selected,temp],axis=1)
        selected=pd.merge(selected,temp,left_on='census_block_group',right_on='census_block_group',how='left')
    except Exception as e:
        print(e)
        print('pass',table)

currentCols = selected.columns.tolist()

newCols = [x for x in currentCols if x in iddict.keys()]
selected=selected[newCols]
newCols = [iddict[x] for x in newCols]
selected.columns=newCols
selected.to_csv(censusblockpath+'selected.csv',index=False)

