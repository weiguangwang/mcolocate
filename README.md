# mlocate

**1. City Selection**

1.1 Data were downloaded from census:

2017 Population Estimates.xlsx was downloaded from US Census data (https://www.census.gov/data/tables/2017/demo/popest/total-cities-and-towns.html). 
4 state (NC,SC, GA, VA, TN) select_cities.xlsx (detailed city data) was downloaded from US Census data (https://www.census.gov/quickfacts/fact/table/savannahcitygeorgia,sandyspringscitygeorgia,roswellcitygeorgia/POP060210). 
20 cities were selected from 1923 cities in the 4 states.

1.2 manual selection of comparison cities

6 cities were selected by authors through comparing the population size, demographical distribution, and influences of hurricanes in the study periods.

**2. Data Preprocess**


2.1 data filtering

2.1.1 Records outside the two periods were excluded. 
Pre-hurricane period is: July 1st, 2018 – September 13th, 2018 at 12am
Post-hurricane period is: September 15th, 2018 at 12 am

2.1.2 Only users appeared in both pre- and post-hurricane period are included.

2.1.3 Each user should have at least 10 records in either of the two periods. Otherwise, he/she was excluded. 

2.2 Records grouping by location and time. 
A record will be kept only if this point is further away from the previous and the next points than 100 meters. (the length of stay will be summed up)

2.3 Truncate super long stays
If one user stays at one location for more than 24 hours, this will be treated as an invalid stay time. 



**3. Variable Development**


python addPOI_v0.py
python id_date_convert_v1.py	##irrelavant cols are removed, such as the venue category
python calFamilySize.py
python selectOnlyFamily.py
python hourly_v1.py	##big change
python add_family_together_v1.py
python add_block.py

python merge_hourly.py	##multiple records for same user-day-hour will be combined.
python merge_cities.py

python prepareBlockData.py
python bPaper_addBlockData.py


**3. Descriptive Results**

![Family Colocation over Time](https://github.com/weiguangwang/mcolocate/blob/main/fig/Fig1.png)
Fig. 1. Family Colocation over Time
![Family Colocation over Time](https://github.com/weiguangwang/mcolocate/blob/main/fig/Fig2.png)
Fig. 1. Family Colocation over Time
![Family Colocation over Time](https://github.com/weiguangwang/mcolocate/blob/main/fig/Figs1.png)
Fig. 1. Family Colocation over Time
![Family Colocation over Time](https://github.com/weiguangwang/mcolocate/blob/main/fig/Figs2.png)
Fig. 1. Family Colocation over Time







