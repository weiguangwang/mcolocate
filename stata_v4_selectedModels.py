
#import delimited F:\20181110_gpsHealth\process\v3\all_07_11_both_valid10_abouthome_hourly_venue_speed_simpleid_family.csv
#cd "F:\20181110_gpsHealth\process\v3\stataOut"
#save "F:\20181110_gpsHealth\process\v3\stataOut\all.dta"

use "F:\20181110_gpsHealth\process\v3\stataOut\all.dta", clear
cd "F:\20181110_gpsHealth\process\v3\stataOut"

import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.csv"
use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta"
cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
use "H:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta"
cd "H:\20181110_gpsHealth\process\v3\stataOut"


# import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
# cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
drop dist_home_avg placeid nearestdist blockfips


egen ncity = group(city)
#tab ncity city
#cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
#chattanooga, knoxville, and charleston were partially influenced. 
#ne-1;sa-2;wi-3



#xtset advertiser_id


gen post = 0 if date <= 75
replace post = 1 if date >= 77
drop if post == .

gen treated = 0
replace treated = 1 if city == "wi"
gen partialTreated = 0
replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
gen notTreated = 0
replace notTreated = 1 if city == "sa" | city == "ne"

gen treatedPost = post * treated
#gen partialTreatedPost = post * partialTreated
gen notTreatedPost = post * notTreated

# gen togethorB = 0
# replace togethorB = 1 if outtogethor > 0


xtset advertiser_id

##this is for table 2 in 20201010
def main():
    drop if partialTreated == 1
    drop partialTreated
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    margins, dydx(post) at(treated=1) vsquish   #dy/dx = .0785128, p<0.00
    #clogit athome post treated treatedPost i.hour numspeeds_no0, group(advertiser_id) robust cluster(advertiser_id)
    outreg2 using report_table1.doc, replace ctitle('main-fe')


###



##this is for table 3 in 20201010
def overTime_TC():
    preserve
    drop if date >= 77+7
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table2.doc, replace ctitle('main-one week')
    restore


    preserve
    drop if date >= 77+30
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table2.doc, ctitle('main-one month')
    restore


    preserve
    drop if (date < 77+30 & date >= 77)
    drop if date >= 77+60
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table2.doc, ctitle('main-month 2nd')
    restore


    preserve
    drop if (date < 77+60 & date >= 77)
    drop if date >= 77+90
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table2.doc, ctitle('main-month 3rd')
    restore



###






def genTimeOfDay():
    #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
    
    gen morning = 0
    replace morning = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
    replace morning = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
    replace morning = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

    replace morning = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
    replace morning = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
    replace morning = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
    replace morning = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

    replace morning = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
    replace morning = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
    replace morning = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

    replace morning = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
    replace morning = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
    replace morning = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
    replace morning = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

    replace morning = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
    replace morning = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
    replace morning = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

    replace morning = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
    replace morning = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
    replace morning = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
    replace morning = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12


    gen earlymorning = 0
    replace earlymorning = 1 if city == "wi" & date <= 85 & hour <= 6
    replace earlymorning = 1 if city == "wi" & date > 85 & date <= 127 & hour <= 7
    replace earlymorning = 1 if city == "wi" & date > 127 & date <= 154 & hour <= 6

    replace earlymorning = 1 if city == "ct" & date <= 45 & hour <= 6
    replace earlymorning = 1 if city == "ct" & date > 45 & date <= 122 & hour <= 7
    replace earlymorning = 1 if city == "ct" & date > 122 & date <= 127 & hour <= 8
    replace earlymorning = 1 if city == "ct" & date > 127 & date <= 154 & hour <= 7

    replace earlymorning = 1 if city == "cl" & date <= 72 & hour <= 6
    replace earlymorning = 1 if city == "cl" & date > 72 & date <= 127 & hour <= 7
    replace earlymorning = 1 if city == "cl" & date > 127 & date <= 154 & hour <= 6

    replace earlymorning = 1 if city == "kn" & date <= 54 & hour <= 6
    replace earlymorning = 1 if city == "kn" & date > 54 & date <= 126 & hour <= 7
    replace earlymorning = 1 if city == "kn" & date > 126 & date <= 127 & hour <= 8
    replace earlymorning = 1 if city == "kn" & date > 127 & date <= 154 & hour <= 7

    replace earlymorning = 1 if city == "sa" & date <= 64 & hour <= 6
    replace earlymorning = 1 if city == "sa" & date > 64 & date <= 127 & hour <= 7
    replace earlymorning = 1 if city == "sa" & date > 127 & date <= 154 & hour <= 6

    replace earlymorning = 1 if city == "ne" & date <= 18 & hour <= 5
    replace earlymorning = 1 if city == "ne" & date > 18 & date <= 92 & hour <= 6
    replace earlymorning = 1 if city == "ne" & date > 92 & date <= 127 & hour <= 7
    replace earlymorning = 1 if city == "ne" & date > 127 & date <= 154 & hour <= 6



    gen afternoon = 0
    replace afternoon = 1 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
    replace afternoon = 1 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


    gen night = 0
    replace night = 1 if city == "wi" & date <= 45 & hour >= 20 
    replace night = 1 if city == "wi" & date > 45 & date <= 91 & hour >= 19 
    replace night = 1 if city == "wi" & date > 91 & date <= 127 & hour >= 18 
    replace night = 1 if city == "wi" & date > 127 & date <= 154 & hour >= 17 

    replace night = 1 if city == "ct" & date <= 69 & hour >= 20 
    replace night = 1 if city == "ct" & date > 69 & date <= 113 & hour >= 19 
    replace night = 1 if city == "ct" & date > 113 & date <= 127 & hour >= 18 
    replace night = 1 if city == "ct" & date > 127 & date <= 154 & hour >= 17 

    replace night = 1 if city == "cl" & date <= 51 & hour >= 20 
    replace night = 1 if city == "cl" & date > 51 & date <= 97 & hour >= 19 
    replace night = 1 if city == "cl" & date > 97 & date <= 127 & hour >= 18 
    replace night = 1 if city == "cl" & date > 127 & date <= 154 & hour >= 17 

    replace night = 1 if city == "kn" & date <= 66 & hour >= 20 
    replace night = 1 if city == "kn" & date > 66 & date <= 107 & hour >= 19 
    replace night = 1 if city == "kn" & date > 107 & date <= 127 & hour >= 18 
    replace night = 1 if city == "kn" & date > 127 & date <= 154 & hour >= 17 

    replace night = 1 if city == "sa" & date <= 54 & hour >= 20 
    replace night = 1 if city == "sa" & date > 54 & date <= 101 & hour >= 19 
    replace night = 1 if city == "sa" & date > 101 & date <= 127 & hour >= 18 
    replace night = 1 if city == "sa" & date > 127 & date <= 154 & hour >= 17 

    replace night = 1 if city == "ne" & date <= 44 & hour >= 20 
    replace night = 1 if city == "ne" & date > 44 & date <= 86 & hour >= 19 
    replace night = 1 if city == "ne" & date > 86 & date <= 127 & hour >= 18 
    replace night = 1 if city == "ne" & date > 127 & date <= 133 & hour >= 17 
    replace night = 1 if city == "ne" & date > 133 & date <= 154 & hour >= 16 

###

def genDayOfWeek():
    gen weekend = 0
    replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

###    
#
# drop city
# drop date


def subgroup_tod_dow():
    use "D:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta" 
    cd "D:\20181110_gpsHealth\process\v3\stataOut"
    drop dist_home_avg placeid nearestdist blockfips
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"

    gen treatedPost = post * treated
    #gen partialTreatedPost = post * partialTreated
    gen notTreatedPost = post * notTreated


    xtset advertiser_id

    preserve
    keep if weekend ==0
    keep if morning == 1 | afternoon ==1
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_subgroup_tod_dow.doc, replace ctitle('day-weekday')
    restore
    preserve
    keep if weekend ==0
    keep if earlymorning == 1 | night ==1
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_subgroup_tod_dow.doc, ctitle('night-weekday')
    restore
    preserve
    keep if weekend ==1
    keep if morning == 1 | afternoon ==1
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_subgroup_tod_dow.doc, ctitle('day-weekend')
    restore
    preserve
    keep if weekend ==1
    keep if earlymorning == 1 | night ==1
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_subgroup_tod_dow.doc, ctitle('night-weekend')
    restore

###



def moderateTimeOfDay():
    gen modEarlymorning = treatedPost * earlymorning
    gen modMorning = treatedPost * morning
    gen modAfternoon = treatedPost * afternoon
    gen modNight = treatedPost * night
    
    gen postEarlymorning = post * earlymorning
    gen postMorning = post * morning
    gen postAfternoon = post * afternoon
    gen postNight = post * night
    
    gen treatedEarlymorning = treated * earlymorning
    gen treatedMorning = treated * morning
    gen treatedAfternoon = treated * afternoon
    gen treatedNight = treated * night
    
    xtreg togetherb_avg earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight i.hour post, fe robust cluster(advertiser_id)
    outreg2 using report_tables2.doc, ctitle('moderate-tod')
    
    
    gen modWeekend = treatedPost * weekend
    gen postWeekend = post * weekend
    gen treatedWeekend = treated * weekend
    xtreg togetherb_avg weekend modWeekend postWeekend treatedWeekend post treatedPost, fe robust cluster(advertiser_id)
    outreg2 using report_tables2.doc, ctitle('moderate-weekend')
    
    gen daytime = .
    replace daytime = 0 if earlymorning == 1
    replace daytime = 0 if night == 1
    replace daytime = 1 if morning == 1
    replace daytime = 1 if afternoon == 1
    gen nighttime = .
    replace nighttime = 1 if earlymorning == 1
    replace nighttime = 1 if night == 1
    replace nighttime = 0 if morning == 1
    replace nighttime = 0 if afternoon == 1
    gen modDaytime = treatedPost * daytime
    gen postDaytime = post * daytime
    gen treatedDaytime = treated * daytime
    gen modPartialDaytime = partialTreatedPost * daytime
    gen PartialtreatedDaytime = partialTreated * daytime
    gen modNighttime = treatedPost * nighttime
    gen postNighttime = post * nighttime
    gen treatedNighttime = treated * nighttime
    gen modPartialNighttime = partialTreatedPost * nighttime
    gen PartialtreatedNighttime = partialTreated * nighttime
    
    xtreg togetherb_avg daytime nighttime modDaytime modNighttime postDaytime postNighttime treatedDaytime treatedNighttime i.hour post, fe robust cluster(advertiser_id)
    outreg2 using report_tables2.doc, ctitle('moderate-dayNight')

    xtreg togetherb_avg nighttime modNighttime postNighttime treatedNighttime post treatedPost, fe robust cluster(advertiser_id)
    outreg2 using report_tables2.doc, ctitle('moderate-nighttime')
    
    
    gen weekendDay = 0
    gen weekdayDay = 0
    gen weekendNight = 0
    gen weekdayNight = 0
    replace weekendDay = 1 if daytime == 1 and weekend == 1
    replace weekdayDay = 1 if daytime == 1 and weekend == 0
    replace weekendNight = 1 if nighttime == 1 and weekend == 1
    replace weekdayNight = 1 if nighttime == 1 and weekend == 0
    gen modWeekendDay = treatedPost * weekendDay
    gen postWeekendDay = post * weekendDay
    gen treatedWeekendDay = treated * weekendDay
    gen modPartialWeekendDay = partialTreatedPost * weekendDay
    gen PartialtreatedWeekendDay = partialTreated * weekendDay
    
    gen modWeekdayDay = treatedPost * weekdayDay
    gen postWeekdayDay = post * weekdayDay
    gen treatedWeekdayDay = treated * weekdayDay
    gen modPartialWeekdayDay = partialTreatedPost * weekdayDay
    gen PartialtreatedWeekdayDay = partialTreated * weekdayDay
    
    gen modWeekendNight = treatedPost * weekendNight
    gen postWeekendNight = post * weekendNight
    gen treatedWeekendNight = treated * weekendNight
    gen modPartialWeekendNight = partialTreatedPost * weekendNight
    gen PartialtreatedWeekendNight = partialTreated * weekendNight
    
    gen modWeekdayNight = treatedPost * weekdayNight
    gen postWeekdayNight = post * weekdayNight
    gen treatedWeekdayNight = treated * weekdayNight
    gen modPartialWeekdayNight = partialTreatedPost * weekdayNight
    gen PartialtreatedWeekdayNight = partialTreated * weekdayNight
    
    xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight i.hour post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
    outreg2 using report_tables2.doc, ctitle('moderate-4 time')
    
    


    def overTime_TC():
        preserve
        drop if date >= 77+7
        xtreg togetherb_avg daytime nighttime modDaytime modNighttime postDaytime postNighttime treatedDaytime treatedNighttime i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime.doc, replace ctitle('moderate-dayNight one week')

        # xtreg togetherb_avg nighttime modNighttime postNighttime treatedNighttime post treatedPost, fe robust cluster(advertiser_id)
        # outreg2 using report_tables2_overtime.doc, ctitle('moderate-nighttime one week')
        xtreg togetherb_avg weekend modWeekend postWeekend treatedWeekend post treatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime.doc, ctitle('moderate-weekend one week')
        restore

        preserve
        drop if date >= 77+30
        xtreg togetherb_avg daytime nighttime modDaytime modNighttime postDaytime postNighttime treatedDaytime treatedNighttime i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime.doc, ctitle('moderate-dayNight one month')

        # xtreg togetherb_avg nighttime modNighttime postNighttime treatedNighttime post treatedPost, fe robust cluster(advertiser_id)
        # outreg2 using report_tables2_overtime.doc, ctitle('moderate-nighttime one month')
        xtreg togetherb_avg weekend modWeekend postWeekend treatedWeekend post treatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime.doc, ctitle('moderate-weekend one month')
        restore

        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg daytime nighttime modDaytime modNighttime postDaytime postNighttime treatedDaytime treatedNighttime i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime.doc, ctitle('moderate-dayNight month 2nd')

        # xtreg togetherb_avg nighttime modNighttime postNighttime treatedNighttime post treatedPost, fe robust cluster(advertiser_id)
        # outreg2 using report_tables2_overtime.doc, ctitle('moderate-nighttime month 2nd')
        xtreg togetherb_avg weekend modWeekend postWeekend treatedWeekend post treatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime.doc, ctitle('moderate-weekend month 2nd')
        restore

        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg daytime nighttime modDaytime modNighttime postDaytime postNighttime treatedDaytime treatedNighttime i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime.doc, ctitle('moderate-dayNight month 3rd')

        # xtreg togetherb_avg nighttime modNighttime postNighttime treatedNighttime post treatedPost, fe robust cluster(advertiser_id)
        # outreg2 using report_tables2_overtime.doc, ctitle('moderate-nighttime month 3rd')
        xtreg togetherb_avg weekend modWeekend postWeekend treatedWeekend post treatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime.doc, ctitle('moderate-weekend month 3rd')
        restore



    def overTime_TC_4time():
        preserve
        drop if date >= 77+7
        xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime_4time.doc, replace ctitle('moderate-dayNight one week')
        restore

        preserve
        drop if date >= 77+30
        xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime_4time.doc, ctitle('moderate-dayNight one month')
        restore

        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime_4time.doc, ctitle('moderate-dayNight month 2nd')
        restore

        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_tables2_overtime_4time.doc, ctitle('moderate-dayNight month 3rd')
        restore



###


def athome_mod():
    gen modAthome = treatedPost * athomeavg
    gen postAthome = post * athomeavg
    gen treatedAthome = treated * athomeavg
    xtreg togetherb_avg post treatedPost postAthome treatedAthome athomeavg modAthome i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_tables3.doc, ctitle('moderate-athome')
    drop modAthome postAthome treatedAthome

    # gen modEarlymorningAthome = athomeavg * modEarlymorning
    # gen modMorningAthome = athomeavg * modMorning
    # gen modAfternoonAthome = athomeavg * modAfternoon
    # gen modNightAthome = athomeavg * modNight
    # gen EarlymorningAthome = athomeavg * earlymorning
    # gen MorningAthome = athomeavg * morning
    # gen AfternoonAthome = athomeavg * afternoon
    # gen NightAthome = athomeavg * night
    # xtreg togetherb_avg earlymorning morning afternoon night postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight modEarlymorning modMorning modAfternoon modNight treatedPost postAthome treatedAthome EarlymorningAthome MorningAthome AfternoonAthome NightAthome modEarlymorningAthome modMorningAthome modAfternoonAthome modNightAthome post treated i.hour, fe robust cluster(advertiser_id)
    # outreg2 using table4.doc, ctitle('moderate-athome') dec(2)
    #
    # drop modEarlymorningAthome modMorningAthome modAfternoonAthome modNightAthome EarlymorningAthome MorningAthome AfternoonAthome NightAthome

    
    preserve
    keep if athomeavg ==1
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables3.doc, ctitle('totallyathome')
    #logit togethorB post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #outreg2 using table5.doc, ctitle('athome') dec(2)
    xtreg togetherb_avg earlymorning morning afternoon night postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight  modEarlymorning modMorning modAfternoon modNight i.hour post, fe robust cluster(advertiser_id)
    #xtlogit athome post treated earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables3.doc, ctitle('totallyathome')
    xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight i.hour post, fe robust cluster(advertiser_id)
    outreg2 using report_tables3.doc, ctitle('totallyathome')
    restore
    preserve
    keep if athomeavg > 0 & athomeavg != .
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables3.doc, ctitle('athome')
    #logit togethorB post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #outreg2 using table5.doc, ctitle('athome') dec(2)
    xtreg togetherb_avg earlymorning morning afternoon night postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight  modEarlymorning modMorning modAfternoon modNight i.hour post, fe robust cluster(advertiser_id)
    #xtlogit athome post treated earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables3.doc, ctitle('athome')
    restore
    preserve
    keep if athome == 0
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables3.doc, ctitle('not athome')
    #logit togethorB post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #outreg2 using table5.doc, ctitle('not athome') dec(2)
    xtreg togetherb_avg earlymorning morning afternoon night postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight  modEarlymorning modMorning modAfternoon modNight i.hour post, fe robust cluster(advertiser_id)
    #xtlogit athome post treated earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables3.doc, ctitle('not athome')
    xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight i.hour post, fe robust cluster(advertiser_id)
    outreg2 using report_tables3.doc, ctitle('totallyathome')
    restore
    
###


def athome_as_dv():
    reg athomeavg post treated treatedPost i.hour, robust cluster(advertiser_id)
    # margins, dydx(post) at(treated=1) vsquish   #dy/dx = .1693934, p<0.00
    outreg2 using table6.doc, replace ctitle('main') dec(2)
    xtreg athomeavg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # margins, dydx(post) at(treated=1) vsquish   #dy/dx = .0785128, p<0.00
    #clogit athome post treated treatedPost i.hour numspeeds_no0, group(advertiser_id) robust cluster(advertiser_id)
    outreg2 using table6.doc, ctitle('main-fe') dec(2)
    
    xtreg athomeavg earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight post treated, fe robust cluster(advertiser_id)
    outreg2 using table6.doc, ctitle('moderate-tod') dec(2)
    
    xtreg athomeavg weekend modWeekend postWeekend treatedWeekend post treated treatedPost, fe robust cluster(advertiser_id)
    #xtlogit togethorB post treated earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using table6.doc, ctitle('moderate-weekend') dec(2)


    xtreg athomeavg post treated treatedPost i.hour i.date i.ncity, fe robust cluster(advertiser_id)
    outreg2 using table6.doc, ctitle('main-fe-control') dec(2)


    xtreg athomeavg post treated treatedPost familysize i.hour i.date i.ncity, fe robust cluster(advertiser_id)
    outreg2 using table6.doc, ctitle('main-fe-control-familysize') dec(2)



    drop modNight modMorning modAfternoon modEarlymorning



def homedist_as_dv():
    import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.csv"
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    
    # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
    # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop placeid nearestdist blockfips speed_avg speed_max togetherb_avg athomeavg
    
    egen ncity = group(city)
    #tab ncity city
    #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
    #chattanooga, knoxville, and charleston were partially influenced. 
    #ne-1;sa-2;wi-3
    
    xtset advertiser_id
    
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    gen treated = 0
    replace treated = 1 if city == "wi"
    gen partialTreated = 0
    replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"
    
    gen treatedPost = post * treated
    #gen partialTreatedPost = post * partialTreated
    gen notTreatedPost = post * notTreated
    reg dist_home_avg post treated treatedPost i.hour, robust cluster(advertiser_id)
    # margins, dydx(post) at(treated=1) vsquish   #dy/dx = .1693934, p<0.00
    outreg2 using homedist_as_dv.doc, replace ctitle('main') dec(2)
    xtreg dist_home_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # margins, dydx(post) at(treated=1) vsquish   #dy/dx = .0785128, p<0.00
    #clogit athome post treated treatedPost i.hour numspeeds_no0, group(advertiser_id) robust cluster(advertiser_id)
    outreg2 using homedist_as_dv.doc, ctitle('main-fe') dec(2)
    
    gen modEarlymorning = treatedPost * earlymorning
    gen modMorning = treatedPost * morning
    gen modAfternoon = treatedPost * afternoon
    gen modNight = treatedPost * night
    
    gen postEarlymorning = post * earlymorning
    gen postMorning = post * morning
    gen postAfternoon = post * afternoon
    gen postNight = post * night
    
    gen treatedEarlymorning = treated * earlymorning
    gen treatedMorning = treated * morning
    gen treatedAfternoon = treated * afternoon
    gen treatedNight = treated * night
    xtreg dist_home_avg earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight post treated, fe robust cluster(advertiser_id)
    outreg2 using homedist_as_dv.doc, ctitle('moderate-tod') dec(2)
    
    gen modWeekend = treatedPost * weekend
    gen postWeekend = post * weekend
    gen treatedWeekend = treated * weekend
    xtreg dist_home_avg weekend modWeekend postWeekend treatedWeekend post treated treatedPost, fe robust cluster(advertiser_id)
    #xtlogit togethorB post treated earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using homedist_as_dv.doc, ctitle('moderate-weekend') dec(2)

    
    xtreg dist_home_avg post treated treatedPost i.hour i.date i.ncity, fe robust cluster(advertiser_id)
    outreg2 using homedist_as_dv.doc, ctitle('main-fe-control') dec(2)


    xtreg dist_home_avg post treated treatedPost familysize i.hour i.date i.ncity, fe robust cluster(advertiser_id)
    outreg2 using homedist_as_dv.doc, ctitle('main-fe-control-familysize') dec(2)
    
    
    def partial()
        import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop blockfips
        drop speed_avg speed_max
        # drop athomeavg
        drop familysize
        
        # egen ncity = group(city)
        # tab ncity city
        #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
        #chattanooga, knoxville, and charleston were partially influenced. 
        #ne-1;sa-2;wi-3
        
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        
        drop city
        # drop date dist_home maxspeeds avgspeeds_no0 city
        drop post notTreated
        drop athomeavg togetherb_avg
        ###

        xtset advertiser_id
        xtreg dist_home_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.0301
        test notTreatedPost == treatedPost  
        #p<0.0016
        test notTreatedPost == partialTreated  
        #p<0.0467

        outreg2 using homedist_as_dv1.doc, ctitle('partial-main-fe') dec(2)


    def overTime_TC():
        preserve
        drop if date >= 77+7
        xtreg dist_home_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using homedist_as_dv21.doc, ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg dist_home_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using homedist_as_dv21.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg dist_home_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using homedist_as_dv21.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg dist_home_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using homedist_as_dv21.doc, ctitle('main-month 3rd') dec(2)
        restore


    def overTimeEffect():
        preserve
        drop if date >= 77+7
        xtreg dist_home_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        test treatedPost = partialTreatedPost
        outreg2 using homedist_as_dv2.doc, ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg dist_home_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        test treatedPost = partialTreatedPost   #0.0713
        outreg2 using homedist_as_dv2.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg dist_home_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        test treatedPost = partialTreatedPost
        outreg2 using homedist_as_dv2.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg dist_home_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        test treatedPost = partialTreatedPost
        outreg2 using homedist_as_dv2.doc, ctitle('main-month 3rd') dec(2)
        restore



    def mod_blcokData():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta"
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"


        drop blockfips familymarriedhaskidrate athomeavg


        # egen ncity = group(city)
        #tab ncity city
        #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
        #chattanooga, knoxville, and charleston were partially influenced. 
        #ne-1;sa-2;wi-3

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        #gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        # gen togethorB = 0
        # replace togethorB = 1 if outtogethor > 0
        drop city date

        drop employmentcivilianrate    yearbuiltmedian  plumbingcompleterate commutetime  commutewalkrate povertybelowrate 
        drop maritaldrate vehiclenumberpercapita maritalwidowedrate
        drop vacancy4occasionalrate vacancy4salerate vacancy4rentrate
        drop togetherb_avg familyhaskidrate raceblackrate eduhighbelowrate fulltimeemploymentrate employmentrate marriedspousepresentrate commutehomerate 
        
        xtset advertiser_id

        gen modIncomemedian = treatedPost * incomemedian
        gen postIncomemedian = post * incomemedian
        gen treatIncomemedian = treated * incomemedian
        xtreg dist_home_avg modIncomemedian incomemedian postIncomemedian treatIncomemedian post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using homedist_as_dv3.doc, ctitle('modIncomeMedian') dec(2)
        drop incomemedian modIncomemedian postIncomemedian treatIncomemedian
        
        gen modvacancyrate = treatedPost * vacancyrate
        gen postvacancyrate = post * vacancyrate
        gen treatvacancyrate = treated * vacancyrate
        xtreg dist_home_avg modvacancyrate vacancyrate postvacancyrate treatvacancyrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using homedist_as_dv3.doc, ctitle('modvacancyrate') dec(2)
        drop modvacancyrate vacancyrate postvacancyrate treatvacancyrate


        gen modcommutepublicrate = treatedPost * commutepublicrate
        gen postcommutepublicrate = post * commutepublicrate
        gen treatcommutepublicrate = treated * commutepublicrate
        xtreg dist_home_avg modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using homedist_as_dv3.doc, ctitle('modcommutepublicrate') dec(2)
        drop modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate

###







    def python_plot():
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        drop hour speed_avg speed_max familysize athomeavg togetherb_avg blockfips advertiser_id
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .
        
        gen group = .
        replace group = 2 if city == "wi"
        replace group = 1 if city == "cl" | city == "ct" | city == "kn"
        replace group = 0 if city == "sa" | city == "ne"
        
        
        gen weeknumber = .
        replace weeknumber = 26 if date == 1
        replace weeknumber = 27 if date >= 2 & date <= 8
        replace weeknumber = 28 if date >= 9 & date <= 15
        replace weeknumber = 29 if date >= 16 & date <= 22
        replace weeknumber = 30 if date >= 23 & date <= 29
        replace weeknumber = 31 if date >= 30 & date <= 36
        replace weeknumber = 32 if date >= 37 & date <= 43
        replace weeknumber = 33 if date >= 44 & date <= 50
        replace weeknumber = 34 if date >= 51 & date <= 57
        replace weeknumber = 35 if date >= 58 & date <= 64
        replace weeknumber = 36 if date >= 65 & date <= 71
        replace weeknumber = 37 if date >= 72 & date <= 78
        replace weeknumber = 38 if date >= 79 & date <= 85
        replace weeknumber = 39 if date >= 86 & date <= 92
        replace weeknumber = 40 if date >= 93 & date <= 99
        replace weeknumber = 41 if date >= 100 & date <= 106
        replace weeknumber = 42 if date >= 107 & date <= 113
        replace weeknumber = 43 if date >= 114 & date <= 120
        replace weeknumber = 44 if date >= 121 & date <= 127
        replace weeknumber = 45 if date >= 128 & date <= 134
        replace weeknumber = 46 if date >= 135 & date <= 141
        replace weeknumber = 47 if date >= 142 & date <= 148
        replace weeknumber = 48 if date >= 149 & date <= 154
        
        drop post 
        
        mean dist_home_avg if group == 0, over(weeknumber)
        mean dist_home_avg if group == 1, over(weeknumber)
        mean dist_home_avg if group == 2, over(weeknumber)
        mean dist_home_avg if city == "wi", over(weeknumber)
        mean dist_home_avg if city == "cl", over(weeknumber)
        mean dist_home_avg if city == "ct", over(weeknumber)
        mean dist_home_avg if city == "kn", over(weeknumber)
        mean dist_home_avg if city == "sa", over(weeknumber)
        mean dist_home_avg if city == "ne", over(weeknumber)



def vehicle():
    gen vehicle = 0
    replace vehicle = 1 if speed_avg > 3
    #replace vehicle = 1 if maxspeeds > 3
    gen modVehicle = treatedPost * vehicle
    gen postVehicle = post * vehicle
    gen treatedVehicle = treated * vehicle
    
    xtreg togetherb_avg vehicle modVehicle postVehicle treatedVehicle i.hour post treated treatedPost, fe robust cluster(advertiser_id)
    outreg2 using table7.doc, replace ctitle('moderate-vehicle-avgSpeed') dec(2)
    xtreg togetherb_avg vehicle modVehicle postVehicle treatedVehicle post treated treatedPost, fe robust cluster(advertiser_id)
    outreg2 using table7.doc, ctitle('moderate-vehicle-avgSpeed') dec(2)
    
    drop vehicle modVehicle postVehicle treatedVehicle
    gen vehicle = 0
    #replace vehicle = 1 if avgspeeds_no0 > 3
    replace vehicle = 1 if speed_max > 3
    gen modVehicle = treatedPost * vehicle
    gen postVehicle = post * vehicle
    gen treatedVehicle = treated * vehicle
    xtreg togetherb_avg vehicle modVehicle postVehicle treatedVehicle i.hour post treated treatedPost, fe robust cluster(advertiser_id)
    outreg2 using table7.doc, ctitle('moderate-vehicle-maxSpeed') dec(2)
    xtreg togetherb_avg vehicle modVehicle postVehicle treatedVehicle post treated treatedPost, fe robust cluster(advertiser_id)
    outreg2 using table7.doc, ctitle('moderate-vehicle-maxSpeed') dec(2)
    









##########################partially treated
def partially treated():

    def read_clean_data():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        use "F:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta"
        cd "F:\20181110_gpsHealth\process\v3\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        # drop athomeavg
        # drop familysize
        
        egen ncity = group(city)
        tab ncity city
        #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
        #chattanooga, knoxville, and charleston were partially influenced. 
        #ne-1;sa-2;wi-3
        
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        
        # drop city
        drop dist_home maxspeeds avgspeeds_no0
        # drop post notTreated
        
    ###

    drop ncity


    #main result
    # reg togetherb_avg post treatedPost partialTreatedPost i.hour, robust cluster(advertiser_id)
    # #xtlogit athome treated notTreatedPost partialTreated treatedPost partialTreatedPost i.hour numspeeds_no0, robust cluster(advertiser_id)
    # test partialTreated == treatedPost
    # #p<0.00
    # test notTreatedPost == treatedPost
    # #p<0.00
    # test notTreatedPost == partialTreated
    # #p<0.00
    # outreg2 using report_table1.doc, ctitle('partial-main') dec(2)

    xtset advertiser_id
    xtreg togetherb_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    # test partialTreated == treatedPost
    # #p<0.01
    # test notTreatedPost == treatedPost
    # #p<0.01
    # test notTreatedPost == partialTreated
    #p<0.01

    outreg2 using report_table1.doc, ctitle('partial-main-fe')





###


# short term vs long term
def overTimeEffect():
    preserve
    drop if date >= 77+7
    xtreg togetherb_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table2.doc, ctitle('main-one week')
    restore


    preserve
    drop if date >= 77+30
    xtreg togetherb_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table2.doc, ctitle('main-one month')
    restore



    preserve
    drop if (date < 77+30 & date >= 77)
    drop if date >= 77+60
    xtreg togetherb_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table2.doc, ctitle('main-month 2nd')
    restore


    preserve
    drop if (date < 77+60 & date >= 77)
    drop if date >= 77+90
    xtreg togetherb_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table2.doc, ctitle('main-month 3rd')
    restore





###


def genTimeOfDay():
    #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018

    gen morning = 0
    replace morning = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
    replace morning = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
    replace morning = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

    replace morning = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
    replace morning = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
    replace morning = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
    replace morning = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

    replace morning = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
    replace morning = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
    replace morning = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

    replace morning = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
    replace morning = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
    replace morning = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
    replace morning = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

    replace morning = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
    replace morning = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
    replace morning = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

    replace morning = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
    replace morning = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
    replace morning = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
    replace morning = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12


    gen earlymorning = 0
    replace earlymorning = 1 if city == "wi" & date <= 85 & hour <= 6
    replace earlymorning = 1 if city == "wi" & date > 85 & date <= 127 & hour <= 7
    replace earlymorning = 1 if city == "wi" & date > 127 & date <= 154 & hour <= 6

    replace earlymorning = 1 if city == "ct" & date <= 45 & hour <= 6
    replace earlymorning = 1 if city == "ct" & date > 45 & date <= 122 & hour <= 7
    replace earlymorning = 1 if city == "ct" & date > 122 & date <= 127 & hour <= 8
    replace earlymorning = 1 if city == "ct" & date > 127 & date <= 154 & hour <= 7

    replace earlymorning = 1 if city == "cl" & date <= 72 & hour <= 6
    replace earlymorning = 1 if city == "cl" & date > 72 & date <= 127 & hour <= 7
    replace earlymorning = 1 if city == "cl" & date > 127 & date <= 154 & hour <= 6

    replace earlymorning = 1 if city == "kn" & date <= 54 & hour <= 6
    replace earlymorning = 1 if city == "kn" & date > 54 & date <= 126 & hour <= 7
    replace earlymorning = 1 if city == "kn" & date > 126 & date <= 127 & hour <= 8
    replace earlymorning = 1 if city == "kn" & date > 127 & date <= 154 & hour <= 7

    replace earlymorning = 1 if city == "sa" & date <= 64 & hour <= 6
    replace earlymorning = 1 if city == "sa" & date > 64 & date <= 127 & hour <= 7
    replace earlymorning = 1 if city == "sa" & date > 127 & date <= 154 & hour <= 6

    replace earlymorning = 1 if city == "ne" & date <= 18 & hour <= 5
    replace earlymorning = 1 if city == "ne" & date > 18 & date <= 92 & hour <= 6
    replace earlymorning = 1 if city == "ne" & date > 92 & date <= 127 & hour <= 7
    replace earlymorning = 1 if city == "ne" & date > 127 & date <= 154 & hour <= 6



    gen afternoon = 0
    replace afternoon = 1 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

    replace afternoon = 1 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
    replace afternoon = 1 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
    replace afternoon = 1 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
    replace afternoon = 1 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
    replace afternoon = 1 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


    gen night = 0
    replace night = 1 if city == "wi" & date <= 45 & hour >= 20
    replace night = 1 if city == "wi" & date > 45 & date <= 91 & hour >= 19
    replace night = 1 if city == "wi" & date > 91 & date <= 127 & hour >= 18
    replace night = 1 if city == "wi" & date > 127 & date <= 154 & hour >= 17

    replace night = 1 if city == "ct" & date <= 69 & hour >= 20
    replace night = 1 if city == "ct" & date > 69 & date <= 113 & hour >= 19
    replace night = 1 if city == "ct" & date > 113 & date <= 127 & hour >= 18
    replace night = 1 if city == "ct" & date > 127 & date <= 154 & hour >= 17

    replace night = 1 if city == "cl" & date <= 51 & hour >= 20
    replace night = 1 if city == "cl" & date > 51 & date <= 97 & hour >= 19
    replace night = 1 if city == "cl" & date > 97 & date <= 127 & hour >= 18
    replace night = 1 if city == "cl" & date > 127 & date <= 154 & hour >= 17

    replace night = 1 if city == "kn" & date <= 66 & hour >= 20
    replace night = 1 if city == "kn" & date > 66 & date <= 107 & hour >= 19
    replace night = 1 if city == "kn" & date > 107 & date <= 127 & hour >= 18
    replace night = 1 if city == "kn" & date > 127 & date <= 154 & hour >= 17

    replace night = 1 if city == "sa" & date <= 54 & hour >= 20
    replace night = 1 if city == "sa" & date > 54 & date <= 101 & hour >= 19
    replace night = 1 if city == "sa" & date > 101 & date <= 127 & hour >= 18
    replace night = 1 if city == "sa" & date > 127 & date <= 154 & hour >= 17

    replace night = 1 if city == "ne" & date <= 44 & hour >= 20
    replace night = 1 if city == "ne" & date > 44 & date <= 86 & hour >= 19
    replace night = 1 if city == "ne" & date > 86 & date <= 127 & hour >= 18
    replace night = 1 if city == "ne" & date > 127 & date <= 133 & hour >= 17
    replace night = 1 if city == "ne" & date > 133 & date <= 154 & hour >= 16

###

def genDayOfWeek():
    gen weekend = 0
    replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

###
#
# drop city
# drop date


##########################together day of week

def moderateTimeOfDay():
    gen modEarlymorning = treatedPost * earlymorning
    gen modMorning = treatedPost * morning
    gen modAfternoon = treatedPost * afternoon
    gen modNight = treatedPost * night

    gen postEarlymorning = post * earlymorning
    gen postMorning = post * morning
    gen postAfternoon = post * afternoon
    gen postNight = post * night

    gen treatedEarlymorning = treated * earlymorning
    gen treatedMorning = treated * morning
    gen treatedAfternoon = treated * afternoon
    gen treatedNight = treated * night

    gen modPartialEarlymorning = partialTreatedPost * earlymorning
    gen modPartialMorning = partialTreatedPost * morning
    gen modPartialAfternoon = partialTreatedPost * afternoon
    gen modPartialNight = partialTreatedPost * night

    gen PartialtreatedEarlymorning = partialTreated * earlymorning
    gen PartialtreatedMorning = partialTreated * morning
    gen PartialtreatedAfternoon = partialTreated * afternoon
    gen PartialtreatedNight = partialTreated * night

    xtreg togetherb_avg earlymorning morning afternoon night postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight  modEarlymorning modMorning modAfternoon modNight modPartialEarlymorning modPartialMorning modPartialAfternoon modPartialNight PartialtreatedEarlymorning PartialtreatedMorning PartialtreatedAfternoon PartialtreatedNight i.hour post, fe robust cluster(advertiser_id)
    outreg2 using report_tables4.doc, ctitle('moderate-tod')


    gen modWeekend = treatedPost * weekend
    gen modPartialWeekend = partialTreatedPost * weekend
    gen postWeekend = post * weekend
    gen treatedWeekend = treated * weekend
    gen PartialtreatedWeekend = partialTreated * weekend
    xtreg togetherb_avg weekend modWeekend modPartialWeekend postWeekend treatedWeekend PartialtreatedWeekend post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
    outreg2 using report_tables4.doc, ctitle('moderate-weekend')


###

def moderateDayNight():
    gen daytime = .
    replace daytime = 0 if earlymorning == 1
    replace daytime = 0 if night == 1
    replace daytime = 1 if morning == 1
    replace daytime = 1 if afternoon == 1
    gen nighttime = .
    replace nighttime = 1 if earlymorning == 1
    replace nighttime = 1 if night == 1
    replace nighttime = 0 if morning == 1
    replace nighttime = 0 if afternoon == 1
    gen modDaytime = treatedPost * daytime
    gen postDaytime = post * daytime
    gen treatedDaytime = treated * daytime
    gen modPartialDaytime = partialTreatedPost * daytime
    gen PartialtreatedDaytime = partialTreated * daytime
    gen modNighttime = treatedPost * nighttime
    gen postNighttime = post * nighttime
    gen treatedNighttime = treated * nighttime
    gen modPartialNighttime = partialTreatedPost * nighttime
    gen PartialtreatedNighttime = partialTreated * nighttime
    
    xtreg togetherb_avg daytime nighttime postDaytime postNighttime treatedDaytime treatedNighttime modDaytime modNighttime modPartialDaytime modPartialNighttime PartialtreatedDaytime PartialtreatedNighttime i.hour post, fe robust cluster(advertiser_id)
    outreg2 using report_dayNight_mod.doc, replace ctitle('moderate-dayNight')

    xtreg togetherb_avg nighttime modNighttime modPartialNighttime postNighttime treatedNighttime PartialtreatedNighttime post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
    outreg2 using report_dayNight_mod.doc, ctitle('moderate-nighttime')

    gen modWeekend = treatedPost * weekend
    gen modPartialWeekend = partialTreatedPost * weekend
    gen postWeekend = post * weekend
    gen treatedWeekend = treated * weekend
    gen PartialtreatedWeekend = partialTreated * weekend
    xtreg togetherb_avg weekend modWeekend modPartialWeekend postWeekend treatedWeekend PartialtreatedWeekend post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
    outreg2 using report_dayNight_mod.doc, ctitle('moderate-weekend')


    gen weekendDay = 0
    gen weekdayDay = 0
    gen weekendNight = 0
    gen weekdayNight = 0
    replace weekendDay = 1 if daytime == 1 and weekend == 1
    replace weekdayDay = 1 if daytime == 1 and weekend == 0
    replace weekendNight = 1 if nighttime == 1 and weekend == 1
    replace weekdayNight = 1 if nighttime == 1 and weekend == 0
    gen modWeekendDay = treatedPost * weekendDay
    gen postWeekendDay = post * weekendDay
    gen treatedWeekendDay = treated * weekendDay
    gen modPartialWeekendDay = partialTreatedPost * weekendDay
    gen PartialtreatedWeekendDay = partialTreated * weekendDay
    
    gen modWeekdayDay = treatedPost * weekdayDay
    gen postWeekdayDay = post * weekdayDay
    gen treatedWeekdayDay = treated * weekdayDay
    gen modPartialWeekdayDay = partialTreatedPost * weekdayDay
    gen PartialtreatedWeekdayDay = partialTreated * weekdayDay
    
    gen modWeekendNight = treatedPost * weekendNight
    gen postWeekendNight = post * weekendNight
    gen treatedWeekendNight = treated * weekendNight
    gen modPartialWeekendNight = partialTreatedPost * weekendNight
    gen PartialtreatedWeekendNight = partialTreated * weekendNight
    
    gen modWeekdayNight = treatedPost * weekdayNight
    gen postWeekdayNight = post * weekdayNight
    gen treatedWeekdayNight = treated * weekdayNight
    gen modPartialWeekdayNight = partialTreatedPost * weekdayNight
    gen PartialtreatedWeekdayNight = partialTreated * weekdayNight
    
    xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight modPartialWeekendDay modPartialWeekdayDay modPartialWeekendNight modPartialWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight PartialtreatedWeekendDay PartialtreatedWeekdayDay PartialtreatedWeekendNight PartialtreatedWeekdayNight i.hour post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
    outreg2 using report_dayNight_mod.doc, ctitle('moderate-4 time')
    

    def overTime_TC():
        preserve
        drop if date >= 77+7
        xtreg togetherb_avg daytime nighttime postDaytime postNighttime treatedDaytime treatedNighttime modDaytime modNighttime modPartialDaytime modPartialNighttime PartialtreatedDaytime PartialtreatedNighttime i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime.doc, replace ctitle('moderate-dayNight one week')

        # xtreg togetherb_avg nighttime modNighttime postNighttime treatedNighttime post treatedPost, fe robust cluster(advertiser_id)
        # outreg2 using report_dayNight_overtime.doc, ctitle('moderate-nighttime one week')
        xtreg togetherb_avg weekend modWeekend modPartialWeekend postWeekend treatedWeekend PartialtreatedWeekend post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime.doc, ctitle('moderate-one week')
        restore

        preserve
        drop if date >= 77+30
        xtreg togetherb_avg daytime nighttime postDaytime postNighttime treatedDaytime treatedNighttime modDaytime modNighttime modPartialDaytime modPartialNighttime PartialtreatedDaytime PartialtreatedNighttime i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime.doc, ctitle('moderate-dayNight one month')

        # xtreg togetherb_avg nighttime modNighttime postNighttime treatedNighttime post treatedPost, fe robust cluster(advertiser_id)
        # outreg2 using report_dayNight_overtime.doc, ctitle('moderate-nighttime one month')
        xtreg togetherb_avg weekend modWeekend modPartialWeekend postWeekend treatedWeekend PartialtreatedWeekend post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime.doc, ctitle('moderate-one month')
        restore

        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg daytime nighttime postDaytime postNighttime treatedDaytime treatedNighttime modDaytime modNighttime modPartialDaytime modPartialNighttime PartialtreatedDaytime PartialtreatedNighttime i.hour post, fe robust cluster(advertiser_id)
        # xtreg togetherb_avg daytime nighttime modDaytime modNighttime postDaytime postNighttime treatedDaytime treatedNighttime i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime.doc, ctitle('moderate-dayNight month 2nd')

        # xtreg togetherb_avg nighttime modNighttime postNighttime treatedNighttime post treatedPost, fe robust cluster(advertiser_id)
        # outreg2 using report_dayNight_overtime.doc, ctitle('moderate-nighttime month 2nd')
        xtreg togetherb_avg weekend modWeekend modPartialWeekend postWeekend treatedWeekend PartialtreatedWeekend post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime.doc, ctitle('moderate-month 2nd')
        restore

        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg daytime nighttime postDaytime postNighttime treatedDaytime treatedNighttime modDaytime modNighttime modPartialDaytime modPartialNighttime PartialtreatedDaytime PartialtreatedNighttime i.hour post, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime.doc, ctitle('moderate-dayNight month 3rd')

        # xtreg togetherb_avg nighttime modNighttime postNighttime treatedNighttime post treatedPost, fe robust cluster(advertiser_id)
        # outreg2 using report_dayNight_overtime.doc, ctitle('moderate-nighttime month 3rd')
        xtreg togetherb_avg weekend modWeekend modPartialWeekend postWeekend treatedWeekend PartialtreatedWeekend post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime.doc, ctitle('moderate-month 3rd')
        restore



    def overTime_TC_4time():
        preserve
        drop if date >= 77+7
        xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight modPartialWeekendDay modPartialWeekdayDay modPartialWeekendNight modPartialWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight PartialtreatedWeekendDay PartialtreatedWeekdayDay PartialtreatedWeekendNight PartialtreatedWeekdayNight i.hour post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime_4time.doc, ctitle('moderate-one week')
        restore

        preserve
        drop if date >= 77+30
        xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight modPartialWeekendDay modPartialWeekdayDay modPartialWeekendNight modPartialWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight PartialtreatedWeekendDay PartialtreatedWeekdayDay PartialtreatedWeekendNight PartialtreatedWeekdayNight i.hour post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime_4time.doc, ctitle('moderate-one month')
        restore

        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight modPartialWeekendDay modPartialWeekdayDay modPartialWeekendNight modPartialWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight PartialtreatedWeekendDay PartialtreatedWeekdayDay PartialtreatedWeekendNight PartialtreatedWeekdayNight i.hour post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime_4time.doc, ctitle('moderate-month 2nd')
        restore

        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight modPartialWeekendDay modPartialWeekdayDay modPartialWeekendNight modPartialWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight PartialtreatedWeekendDay PartialtreatedWeekdayDay PartialtreatedWeekendNight PartialtreatedWeekdayNight i.hour post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        outreg2 using report_dayNight_overtime_4time.doc, ctitle('moderate-month 3rd')
        restore



###

###



def athome_mod()
    gen modAthome = treatedPost * athomeavg
    gen postAthome = post * athomeavg
    gen treatedAthome = treated * athomeavg
    gen modPartialAthome = partialTreatedPost * athomeavg
    gen treatedPartialAthome = partialTreated * athomeavg
    xtreg togetherb_avg post treatedPost partialTreatedPost postAthome treatedAthome athomeavg modAthome modPartialAthome treatedPartialAthome i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_tables5.doc, ctitle('moderate-athome')
    drop modAthome postAthome treatedAthome modPartialAthome treatedPartialAthome


    gen postEarlymorning = post * earlymorning
    gen postMorning = post * morning
    gen postAfternoon = post * afternoon
    gen postNight = post * night

    gen modEarlymorning = treatedPost * earlymorning
    gen modMorning = treatedPost * morning
    gen modAfternoon = treatedPost * afternoon
    gen modNight = treatedPost * night

    gen treatedEarlymorning = treated * earlymorning
    gen treatedMorning = treated * morning
    gen treatedAfternoon = treated * afternoon
    gen treatedNight = treated * night

    gen modPartialEarlymorning = partialTreatedPost * earlymorning
    gen modPartialMorning = partialTreatedPost * morning
    gen modPartialAfternoon = partialTreatedPost * afternoon
    gen modPartialNight = partialTreatedPost * night

    gen PartialtreatedEarlymorning = partialTreated * earlymorning
    gen PartialtreatedMorning = partialTreated * morning
    gen PartialtreatedAfternoon = partialTreated * afternoon
    gen PartialtreatedNight = partialTreated * night



    preserve
    keep if athomeavg ==1
    xtreg togetherb_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables5.doc, ctitle('totallyathome')
    #logit togethorB post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #outreg2 using table5.doc, ctitle('athome') dec(2)
    xtreg togetherb_avg earlymorning morning afternoon night postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight  modEarlymorning modMorning modAfternoon modNight modPartialEarlymorning modPartialMorning modPartialAfternoon modPartialNight PartialtreatedEarlymorning PartialtreatedMorning PartialtreatedAfternoon PartialtreatedNight i.hour post, fe robust cluster(advertiser_id)
    #xtlogit athome post treated earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables5.doc, ctitle('totallyathome')
    xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight modPartialWeekendDay modPartialWeekdayDay modPartialWeekendNight modPartialWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight PartialtreatedWeekendDay PartialtreatedWeekdayDay PartialtreatedWeekendNight PartialtreatedWeekdayNight i.hour post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
    outreg2 using report_tables5.doc, ctitle('totallyathome')
    restore
    preserve
    keep if athome == 0
    xtreg togetherb_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables5.doc, ctitle('not athome')
    #logit togethorB post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #xtlogit athome post treated treatedPost i.hour numspeeds_no0 i.date i.ncity, robust cluster(advertiser_id)
    #outreg2 using table5.doc, ctitle('not athome') dec(2)
    xtreg togetherb_avg earlymorning morning afternoon night postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight  modEarlymorning modMorning modAfternoon modNight modPartialEarlymorning modPartialMorning modPartialAfternoon modPartialNight PartialtreatedEarlymorning PartialtreatedMorning PartialtreatedAfternoon PartialtreatedNight i.hour post, fe robust cluster(advertiser_id)
    #xtlogit athome post treated earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight i.hour numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables5.doc, ctitle('not athome')
    xtreg togetherb_avg weekendDay weekdayDay weekendNight weekdayNight modWeekendDay modWeekdayDay modWeekendNight modWeekdayNight modPartialWeekendDay modPartialWeekdayDay modPartialWeekendNight modPartialWeekdayNight postWeekendDay postWeekdayDay postWeekendNight postWeekdayNight treatedWeekendDay treatedWeekdayDay treatedWeekendNight treatedWeekdayNight PartialtreatedWeekendDay PartialtreatedWeekdayDay PartialtreatedWeekendNight PartialtreatedWeekdayNight i.hour post treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
    outreg2 using report_tables5.doc, ctitle('not athome')
    restore





        

    

#########################census block demographics moderating

    use "D:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta", clear
    cd "D:\20181110_gpsHealth\process\v3\stataOut"


    drop dist_home_avg blockfips familymarriedhaskidrate athomeavg
    keep if date <= 75

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"

    xtset advertiser_id
    # xtreg togetherb_avg incomemedian i.hour, fe robust cluster(advertiser_id)
    
    replace incomemedian = incomemedian / 100000
    gen treatIncomemedian = treated * incomemedian
    gen treatvacancyrate = treated * vacancyrate
    gen treatcommutepublicrate = treated * commutepublicrate
    xtreg togetherb_avg incomemedian vacancyrate commutepublicrate treated i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_initialDisparity.doc, replace ctitle('all')
    xtreg togetherb_avg incomemedian vacancyrate commutepublicrate treated treatIncomemedian treatvacancyrate treatcommutepublicrate i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_initialDisparity.doc, ctitle('modAll')
    xtreg togetherb_avg incomemedian treated treatIncomemedian i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_initialDisparity.doc, ctitle('modIncomeMedian')
    xtreg togetherb_avg vacancyrate treated treatvacancyrate i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_initialDisparity.doc, ctitle('vacancyrate')
    xtreg togetherb_avg commutepublicrate treated treatcommutepublicrate i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_initialDisparity.doc, ctitle('commutepublicrate')



def python_plot_gaps():
    use "D:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta", clear
    cd "D:\20181110_gpsHealth\process\v3\stataOut"
    drop hour speed_avg speed_max familysize athomeavg blockfips advertiser_id
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    gen group = .
    replace group = 2 if city == "wi"
    replace group = 0 if city == "sa" | city == "ne"
    
    
    gen weeknumber = .
    replace weeknumber = 26 if date == 1
    replace weeknumber = 27 if date >= 2 & date <= 8
    replace weeknumber = 28 if date >= 9 & date <= 15
    replace weeknumber = 29 if date >= 16 & date <= 22
    replace weeknumber = 30 if date >= 23 & date <= 29
    replace weeknumber = 31 if date >= 30 & date <= 36
    replace weeknumber = 32 if date >= 37 & date <= 43
    replace weeknumber = 33 if date >= 44 & date <= 50
    replace weeknumber = 34 if date >= 51 & date <= 57
    replace weeknumber = 35 if date >= 58 & date <= 64
    replace weeknumber = 36 if date >= 65 & date <= 71
    replace weeknumber = 37 if date >= 72 & date <= 78
    replace weeknumber = 38 if date >= 79 & date <= 85
    replace weeknumber = 39 if date >= 86 & date <= 92
    replace weeknumber = 40 if date >= 93 & date <= 99
    replace weeknumber = 41 if date >= 100 & date <= 106
    replace weeknumber = 42 if date >= 107 & date <= 113
    replace weeknumber = 43 if date >= 114 & date <= 120
    replace weeknumber = 44 if date >= 121 & date <= 127
    replace weeknumber = 45 if date >= 128 & date <= 134
    replace weeknumber = 46 if date >= 135 & date <= 141
    replace weeknumber = 47 if date >= 142 & date <= 148
    replace weeknumber = 48 if date >= 149 & date <= 154
    
    
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    
    keep if group == 2
    mean togetherb_avg if post == 0, over(blockfips)
    mean togetherb_avg if post == 1, over(blockfips)
    mean incomemedian if post == 0, over(blockfips)
    mean incomemedian if post == 1, over(blockfips)
    
    # replace incomemedian = incomemedian / 100000

    sum incomemedian,d 
    preserve
    #average
    keep if incomemedian >= 61122.46
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore
    preserve
    keep if incomemedian < 61122.46
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore
    preserve
    #median
    keep if incomemedian >= 60350 
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore
    preserve
    keep if incomemedian < 60350 
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore

    sum vacancyrate,d 
    #average
    preserve
    keep if vacancyrate >= .1012114
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore
    preserve
    keep if vacancyrate <  .1012114
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore
    preserve
    #median
    keep if vacancyrate >= .0934744
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore
    preserve
    keep if vacancyrate < .0934744
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore

    sum commutepublicrate,d
    preserve
    #average
    keep if commutepublicrate >= .017874
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore
    preserve
    keep if commutepublicrate <  .017874
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore
    preserve
    #median
    keep if commutepublicrate > 0
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore
    preserve
    keep if commutepublicrate <= 0
    mean togetherb_avg if group == 0, over(post)
    mean togetherb_avg if group == 2, over(post)
    restore


    preserve
    #average
    keep if incomemedian >= 61122.46
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    restore
    preserve
    keep if incomemedian < 61122.46
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    restore
    preserve
    keep if vacancyrate >= .1012114
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    restore
    preserve
    keep if vacancyrate <  .1012114
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    restore
    preserve
    #average
    keep if commutepublicrate >= .017874
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    restore
    preserve
    keep if commutepublicrate <  .017874
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    restore






def mod_blcokData():
    # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block.csv"
    # use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta"
    # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    use "D:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta", clear
    cd "D:\20181110_gpsHealth\process\v3\stataOut"


    drop dist_home_avg blockfips familymarriedhaskidrate athomeavg


    # egen ncity = group(city)
    #tab ncity city
    #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
    #chattanooga, knoxville, and charleston were partially influenced. 
    #ne-1;sa-2;wi-3

    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen partialTreated = 0
    replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"

    gen treatedPost = post * treated
    #gen partialTreatedPost = post * partialTreated
    gen notTreatedPost = post * notTreated

    # gen togethorB = 0
    # replace togethorB = 1 if outtogethor > 0
    drop city date

    drop employmentcivilianrate    yearbuiltmedian  plumbingcompleterate commutetime  commutewalkrate povertybelowrate 
    drop maritaldrate vehiclenumberpercapita maritalwidowedrate
    drop vacancy4occasionalrate vacancy4salerate vacancy4rentrate

    xtset advertiser_id

    replace incomemedian = incomemedian / 100000
    gen modIncomemedian = treatedPost * incomemedian
    gen postIncomemedian = post * incomemedian
    gen treatIncomemedian = treated * incomemedian
    xtreg togetherb_avg modIncomemedian postIncomemedian post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table3.doc, replace ctitle('modIncomeMedian')
    reg togetherb_avg modIncomemedian incomemedian postIncomemedian treatIncomemedian treated post treatedPost i.hour, robust cluster(advertiser_id)
    outreg2 using report_table3.doc, ctitle('modIncomeMedian')
    drop incomemedian modIncomemedian postIncomemedian treatIncomemedian
    
    # gen modPovertybelowrate = treatedPost * povertybelowrate
    # gen postPovertybelowrate = post * povertybelowrate
    # gen treatPovertybelowrate = treated * povertybelowrate
    # xtreg togetherb_avg modPovertybelowrate povertybelowrate postPovertybelowrate treatPovertybelowrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modPovertyBelowRate') dec(2)
    # drop modPovertybelowrate povertybelowrate postPovertybelowrate treatPovertybelowrate
    
    # gen modfamilyhaskidrate = treatedPost * familyhaskidrate
    # gen postfamilyhaskidrate = post * familyhaskidrate
    # gen treatfamilyhaskidrate = treated * familyhaskidrate
    # xtreg togetherb_avg modfamilyhaskidrate familyhaskidrate postfamilyhaskidrate treatfamilyhaskidrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modfamilyhaskidrate') dec(2)
    # drop modfamilyhaskidrate familyhaskidrate postfamilyhaskidrate treatfamilyhaskidrate
    #
    # gen modRaceblackrate = treatedPost * raceblackrate
    # gen postRaceblackrate = post * raceblackrate
    # gen treatRaceblackrate = treated * raceblackrate
    # xtreg togetherb_avg modRaceblackrate raceblackrate postRaceblackrate treatRaceblackrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modRaceBlackRate') dec(2)
    # drop modRaceblackrate raceblackrate postRaceblackrate treatRaceblackrate
    #
    # gen modeduhighbelowrate = treatedPost * eduhighbelowrate
    # gen posteduhighbelowrate = post * eduhighbelowrate
    # gen treateduhighbelowrate = treated * eduhighbelowrate
    # xtreg togetherb_avg modeduhighbelowrate eduhighbelowrate posteduhighbelowrate treateduhighbelowrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modeduhighbelowrate') dec(2)
    # drop modeduhighbelowrate eduhighbelowrate posteduhighbelowrate treateduhighbelowrate
    #
    #
    # gen modemploymentrate = treatedPost * employmentrate
    # gen postemploymentrate = post * employmentrate
    # gen treatemploymentrate = treated * employmentrate
    # xtreg togetherb_avg modemploymentrate employmentrate postemploymentrate treatemploymentrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modemploymentrate') dec(2)
    # drop modemploymentrate employmentrate postemploymentrate treatemploymentrate
    #
    # gen modfulltimeemploymentrate = treatedPost * fulltimeemploymentrate
    # gen postfulltimeemploymentrate = post * fulltimeemploymentrate
    # gen treatfulltimeemploymentrate = treated * fulltimeemploymentrate
    # xtreg togetherb_avg modfulltimeemploymentrate fulltimeemploymentrate postfulltimeemploymentrate treatfulltimeemploymentrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modfulltimeemploymentrate') dec(2)
    # drop modfulltimeemploymentrate fulltimeemploymentrate postfulltimeemploymentrate treatfulltimeemploymentrate
    #
    # gen modmarriedspousepresentrate = treatedPost * marriedspousepresentrate
    # gen postmarriedspousepresentrate = post * marriedspousepresentrate
    # gen treatmarriedspousepresentrate = treated * marriedspousepresentrate
    # xtreg togetherb_avg modmarriedspousepresentrate marriedspousepresentrate postmarriedspousepresentrate treatmarriedspousepresentrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modmarriedspousepresentrate') dec(2)
    # drop modmarriedspousepresentrate marriedspousepresentrate postmarriedspousepresentrate treatmarriedspousepresentrate

    # gen modmaritaldrate = treatedPost * maritaldrate
    # gen postmaritaldrate = post * maritaldrate
    # gen treatmaritaldrate = treated * maritaldrate
    # xtreg togetherb_avg modmaritaldrate maritaldrate postmaritaldrate treatmaritaldrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modmaritaldrate') dec(2)
    # drop modmaritaldrate maritaldrate postmaritaldrate treatmaritaldrate

    # gen modmaritalwidowedrate = treatedPost * maritalwidowedrate
    # gen postmaritalwidowedrate = post * maritalwidowedrate
    # gen treatmaritalwidowedrate = treated * maritalwidowedrate
    # xtreg togetherb_avg modmaritalwidowedrate maritalwidowedrate postmaritalwidowedrate treatmaritalwidowedrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modmaritalwidowedrate') dec(2)
    # drop modmaritalwidowedrate maritalwidowedrate postmaritalwidowedrate treatmaritalwidowedrate

    # gen modvehiclenumberpercapita = treatedPost * vehiclenumberpercapita
    # gen postvehiclenumberpercapita = post * vehiclenumberpercapita
    # gen treatvehiclenumberpercapita = treated * vehiclenumberpercapita
    # xtreg togetherb_avg modvehiclenumberpercapita vehiclenumberpercapita postvehiclenumberpercapita treatvehiclenumberpercapita post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modvehiclenumberpercapita') dec(2)
    # drop modvehiclenumberpercapita vehiclenumberpercapita postvehiclenumberpercapita treatvehiclenumberpercapita

    gen modvacancyrate = treatedPost * vacancyrate
    gen postvacancyrate = post * vacancyrate
    gen treatvacancyrate = treated * vacancyrate
    xtreg togetherb_avg modvacancyrate postvacancyrate post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table3.doc, ctitle('modvacancyrate')
    reg togetherb_avg modvacancyrate vacancyrate postvacancyrate treatvacancyrate post treated treatedPost i.hour, robust cluster(advertiser_id)
    outreg2 using report_table3.doc, ctitle('modvacancyrate')
    drop modvacancyrate vacancyrate postvacancyrate treatvacancyrate


    gen modcommutepublicrate = treatedPost * commutepublicrate
    gen postcommutepublicrate = post * commutepublicrate
    gen treatcommutepublicrate = treated * commutepublicrate
    xtreg togetherb_avg modcommutepublicrate postcommutepublicrate post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using report_table3.doc, ctitle('modcommutepublicrate')
    reg togetherb_avg modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate post treated treatedPost i.hour, robust cluster(advertiser_id)
    outreg2 using report_table3.doc, ctitle('modcommutepublicrate')
    drop modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate


    # gen modcommutehomerate = treatedPost * commutehomerate
    # gen postcommutehomerate = post * commutehomerate
    # gen treatcommutehomerate = treated * commutehomerate
    # xtreg togetherb_avg modcommutehomerate commutehomerate postcommutehomerate treatcommutehomerate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modcommutehomerate') dec(2)
    # drop modcommutehomerate commutehomerate postcommutehomerate treatcommutehomerate
    #
    #
    # gen modvacancy4occasionalrate = treatedPost * vacancy4occasionalrate
    # gen postvacancy4occasionalrate = post * vacancy4occasionalrate
    # gen treatvacancy4occasionalrate = treated * vacancy4occasionalrate
    # xtreg togetherb_avg modvacancy4occasionalrate vacancy4occasionalrate postvacancy4occasionalrate treatvacancy4occasionalrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modvacancy4occasionalrate') dec(2)
    # drop modvacancy4occasionalrate vacancy4occasionalrate postvacancy4occasionalrate treatvacancy4occasionalrate
    #
    #
    # gen modvacancy4salerate = treatedPost * vacancy4salerate
    # gen postvacancy4salerate = post * vacancy4salerate
    # gen treatvacancy4salerate = treated * vacancy4salerate
    # xtreg togetherb_avg modvacancy4salerate vacancy4salerate postvacancy4salerate treatvacancy4salerate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modvacancy4salerate') dec(2)
    # drop modvacancy4salerate vacancy4salerate postvacancy4salerate treatvacancy4salerate
    #
    #
    # gen modvacancy4rentrate = treatedPost * vacancy4rentrate
    # gen postvacancy4rentrate = post * vacancy4rentrate
    # gen treatvacancy4rentrate = treated * vacancy4rentrate
    # xtreg togetherb_avg modvacancy4rentrate vacancy4rentrate postvacancy4rentrate treatvacancy4rentrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using mod_blcokData.doc, ctitle('modvacancy4rentrate') dec(2)
    # drop modvacancy4rentrate vacancy4rentrate postvacancy4rentrate treatvacancy4rentrate






def mmigration():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    drop hour date dist_home_avg speed_avg speed_max familysize athomeavg togetherb_avg blockfips 
    
    keep if city == "wi"
    export delimited using "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut\temp.csv", replace
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    drop hour date dist_home_avg speed_avg speed_max familysize athomeavg togetherb_avg blockfips 
    keep if city == "cl"
    export delimited using "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut\tempcl.csv", replace
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    drop hour date dist_home_avg speed_avg speed_max familysize athomeavg togetherb_avg blockfips 
    keep if city == "ct"
    export delimited using "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut\tempct.csv", replace
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    drop hour date dist_home_avg speed_avg speed_max familysize athomeavg togetherb_avg blockfips 
    keep if city == "kn"
    export delimited using "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut\tempkn.csv", replace
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    drop hour date dist_home_avg speed_avg speed_max familysize athomeavg togetherb_avg blockfips 
    keep if city == "sa"
    export delimited using "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut\tempsa.csv", replace
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    drop hour date dist_home_avg speed_avg speed_max familysize athomeavg togetherb_avg blockfips 
    keep if city == "ne"
    export delimited using "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut\tempne.csv", replace

    def python():
        import pandas as pd
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/temp.csv")
        wiids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempcl.csv")
        clids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempct.csv")
        ctids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempkn.csv")
        knids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempsa.csv")
        saids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempne.csv")
        neids = data['advertiser_id'].unique().tolist()
        del data


        uwiids = [x for x in wiids if x not in clids]
        uwiids = [x for x in uwiids if x not in ctids]
        uwiids = [x for x in uwiids if x not in knids]
        uwiids = [x for x in uwiids if x not in saids]
        uwiids = [x for x in uwiids if x not in neids]
        print(len(wiids),len(uwiids),len(wiids)-len(uwiids), (len(wiids)-len(uwiids))/(len(wiids)))

        uclids = [x for x in clids if x not in wiids]
        uclids = [x for x in uclids if x not in ctids]
        uclids = [x for x in uclids if x not in knids]
        uclids = [x for x in uclids if x not in saids]
        uclids = [x for x in uclids if x not in neids]
        print(len(clids),len(uclids))
        print(len(clids),len(uclids),len(clids)-len(uclids), (len(clids)-len(uclids))/(len(clids)))

        uctids = [x for x in ctids if x not in wiids]
        uctids = [x for x in uctids if x not in clids]
        uctids = [x for x in uctids if x not in knids]
        uctids = [x for x in uctids if x not in saids]
        uctids = [x for x in uctids if x not in neids]
        print(len(ctids),len(uctids))
        print(len(ctids),len(uctids), len(ctids)-len(uctids),(len(ctids)-len(uctids))/(len(ctids)))

        uknids = [x for x in knids if x not in wiids]
        uknids = [x for x in uknids if x not in clids]
        uknids = [x for x in uknids if x not in ctids]
        uknids = [x for x in uknids if x not in saids]
        uknids = [x for x in uknids if x not in neids]
        print(len(knids),len(uknids))
        print(len(knids),len(uknids),len(knids)-len(uknids), (len(knids)-len(uknids))/(len(knids)))

        usaids = [x for x in saids if x not in wiids]
        usaids = [x for x in usaids if x not in clids]
        usaids = [x for x in usaids if x not in ctids]
        usaids = [x for x in usaids if x not in knids]
        usaids = [x for x in usaids if x not in neids]
        print(len(saids),len(usaids))
        print(len(saids),len(usaids), len(saids)-len(usaids), (len(saids)-len(usaids))/(len(saids)))

        uneids = [x for x in neids if x not in wiids]
        uneids = [x for x in uneids if x not in clids]
        uneids = [x for x in uneids if x not in ctids]
        uneids = [x for x in uneids if x not in knids]
        uneids = [x for x in uneids if x not in saids]
        print(len(neids),len(uneids))
        print(len(neids),len(uneids),len(neids)-len(uneids), (len(neids)-len(uneids))/(len(neids)))


        uclids = [x for x in clids if x not in wiids]
        uctids = [x for x in ctids if x not in wiids]
        uknids = [x for x in knids if x not in wiids]
        usaids = [x for x in saids if x not in wiids]
        uneids = [x for x in neids if x not in wiids]
        print(len(clids),len(uclids),len(clids)-len(uclids), (len(clids)-len(uclids))/(len(clids)))
        print(len(ctids),len(uctids), len(ctids)-len(uctids),(len(ctids)-len(uctids))/(len(ctids)))
        print(len(knids),len(uknids),len(knids)-len(uknids), (len(knids)-len(uknids))/(len(knids)))
        print(len(saids),len(usaids), len(saids)-len(usaids), (len(saids)-len(usaids))/(len(saids)))
        print(len(neids),len(uneids),len(neids)-len(uneids), (len(neids)-len(uneids))/(len(neids)))


    def python_removeOverlapped()
        import pandas as pd
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/temp.csv")
        wiids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempcl.csv")
        clids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempct.csv")
        ctids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempkn.csv")
        knids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempsa.csv")
        saids = data['advertiser_id'].unique().tolist()
        del data
        data = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/tempne.csv")
        neids = data['advertiser_id'].unique().tolist()
        del data

        allids = []
        allids += wiids
        allids += clids
        allids += ctids
        allids += knids
        allids += saids
        allids += neids
        allids = pd.DataFrame(allids)
        allids.columns = ['id']
        overlappedIDs = allids.loc[allids.duplicated()]['id'].unique().tolist()
        print(len(overlappedIDs))
        allids = pd.DataFrame(overlappedIDs)
        allids.to_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/overlappedIDs.csv",index=False)

    def stata_prepareRawdata()
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta"
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"


        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg placeid nearestdist blockfips

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen treated = 0
        replace treated = 1 if city == "wi"
        # gen partialTreated = 0
        # replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        # gen notTreated = 0
        # replace notTreated = 1 if city == "sa" | city == "ne"
        
        drop speed_avg speed_max familysize athomeavg post city date
        export delimited using "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\process\temp.csv", replace


    def python_removeOverlap()
        import pandas as pd
        cols2use = ['advertiser_id', 'hour', 'date', 'togetherB_avg', 'city']
        # data=pd.read_csv('C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/process/temp.csv')
        processpath = 'F:/20181110_gpsHealth/process/v3/'
        data=pd.read_csv(processpath+'s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.csv',usecols = cols2use)
        # overlappedIDs = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/overlappedIDs.csv")['0'].tolist()
        overlappedIDs = pd.read_csv(processpath+"overlappedIDs.csv")['0'].tolist()
        data = data.loc[~data['advertiser_id'].isin(overlappedIDs)]
        data.to_csv(processpath+'s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_noMigrate.csv',index=False)
        
        del data
        data=pd.read_csv(processpath+'s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv',usecols = cols2use)
        # overlappedIDs = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/overlappedIDs.csv")['0'].tolist()
        overlappedIDs = pd.read_csv(processpath+"overlappedIDs.csv")['0'].tolist()
        data = data.loc[~data['advertiser_id'].isin(overlappedIDs)]
        data.to_csv(processpath+'s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC_noMigrate.csv',index=False)
        
        del data
        cols2use = ['advertiser_id', 'hour', 'date', 'togetherB_avg', 'city','incomeMedian', 'vacancyRate', 'vacancy4saleRate', 'vacancy4rentRate', 'commutepublicRate']
        data=pd.read_csv(processpath+'s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block.csv',usecols = cols2use)
        # overlappedIDs = pd.read_csv("C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/result/stataOut/overlappedIDs.csv")['0'].tolist()
        overlappedIDs = pd.read_csv(processpath+"overlappedIDs.csv")['0'].tolist()
        data = data.loc[~data['advertiser_id'].isin(overlappedIDs)]
        data.to_csv(processpath+'s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_noMigrate.csv',index=False)
        
        


def migrationRobust()
    ###
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_noMigrate.dta"
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"


    # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
    # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop dist_home_avg placeid nearestdist blockfips

    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen partialTreated = 0
    replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"

    gen treatedPost = post * treated
    #gen partialTreatedPost = post * partialTreated
    gen notTreatedPost = post * notTreated

    # gen togethorB = 0
    # replace togethorB = 1 if outtogethor > 0

    xtset advertiser_id

    ##this is for table 2 in 20201010
    def main():
        drop if partialTreated == 1
        drop partialTreated
        reg togetherb_avg post treated treatedPost i.hour, robust cluster(advertiser_id)
        margins, dydx(post) at(treated=1) vsquish   #dy/dx = .1693934, p<0.00
        outreg2 using table1.doc, replace ctitle('main') dec(2)
        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        margins, dydx(post) at(treated=1) vsquish   #dy/dx = .0785128, p<0.00
        #clogit athome post treated treatedPost i.hour numspeeds_no0, group(advertiser_id) robust cluster(advertiser_id)
        outreg2 using table1.doc, ctitle('main-fe') dec(2)

        reg togetherb_avg post treated treatedPost i.hour i.date i.ncity, robust cluster(advertiser_id)
        margins, dydx(post) at(treated=1) vsquish   #dy/dx = , p<0.00
        outreg2 using table1.doc, ctitle('main-control') dec(2)

        xtreg togetherb_avg post treated treatedPost i.hour i.date i.ncity, fe robust cluster(advertiser_id)
        margins, dydx(post) at(treated=1) vsquish   #dy/dx = , p<0.00
        outreg2 using table1.doc, ctitle('main-fe-control') dec(2)


        xtreg togetherb_avg post treated treatedPost familysize i.hour i.date i.ncity, fe robust cluster(advertiser_id)
        margins, dydx(post) at(treated=1) vsquish   #dy/dx = , p<0.00
        outreg2 using table1.doc, ctitle('main-fe-control-familysize') dec(2)

    ###


    ##this is for table 3 in 20201010
    def overTime_TC():
        preserve
        drop if date >= 77+7
        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using overTime_TC.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using overTime_TC.doc, ctitle('main-one month') dec(2)
        restore



        preserve
        drop if date >= 77+60
        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using overTime_TC.doc, ctitle('main-two month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using overTime_TC.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using overTime_TC.doc, ctitle('main-month 3rd') dec(2)
        restore





        preserve
        drop if (date < 77+7 & date >= 77)
        drop if date >= 77+14
        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using overTime_TC.doc, ctitle('week2') dec(2)
        restore


        preserve
        drop if (date < 77+14 & date >= 77)
        drop if date >= 77+21
        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using overTime_TC.doc, ctitle('week3') dec(2)
        restore


        preserve
        drop if (date < 77+21 & date >= 77)
        drop if date >= 77+28
        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using overTime_TC.doc, ctitle('week4') dec(2)
        restore

###






def falsificationTest():

    # use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta",clear
    # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"

    use "D:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta",clear
    cd "D:\20181110_gpsHealth\process\v3\stataOut"


    drop dist_home_avg placeid nearestdist blockfips
    drop speed_avg speed_max athomeavg

    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    drop post

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"


    xtset advertiser_id

    def fasi_1m():
        preserve
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop if date < 75-30
        drop if date > 77+30

        gen treatedPost = post * treated

        xtreg togetherb_avg post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_falsification.doc, replace ctitle('9/12') dec(2)

        restore

        preserve
        gen post = 0 if date <= 26
        replace post = 1 if date >= 28
        drop if post == .

        drop if date < 26-25
        drop if date > 28+25

        gen treatedPost = post * treated

        xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_falsification.doc, replace ctitle('7/25')

        restore

        preserve

        gen post = 0 if date <= 40
        replace post = 1 if date >= 42
        drop if post == .

        drop if date < 40-30
        drop if date > 42+30

        gen treatedPost = post * treated

        xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_falsification.doc,  ctitle('8/8')


        restore

        preserve

        gen post = 0 if date <= 54
        replace post = 1 if date >= 56
        drop if post == .

        drop if date < 54-30
        drop if date > 56+30

        gen treatedPost = post * treated

        xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_falsification.doc,  ctitle('8/22')

        restore




###









def familySize():

    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta",clear
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"

    drop dist_home_avg placeid nearestdist blockfips
    drop speed_avg speed_max athomeavg

    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"

    gen treatedPost = post * treated
    gen notTreatedPost = post * notTreated


    xtset advertiser_id
    
    gen modFamilySize = familysize * treatedPost
    gen postFamilySize = familysize * post
    gen treatedFamilySize = familysize * treated
    xtreg togetherb_avg post treatedPost modFamilySize familysize postFamilySize treatedFamilySize i.hour, fe robust cluster(advertiser_id)
    outreg2 using familySize.doc, replace ctitle('familysize')
    
    keep if familysize <= 10
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using familySize.doc, replace ctitle('fam10')

    keep if familysize <= 5
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using familySize.doc, ctitle('fam5')

    keep if familysize <= 4

    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using familySize.doc, ctitle('fam4')

    keep if familysize <= 3
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using familySize.doc, ctitle('fam3')

    keep if familysize <= 2
    xtreg togetherb_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using familySize.doc, ctitle('fam2')


###




#PSmatching does not work
def PSmatching():

    import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block.csv"
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    
    drop nearestdist blockfips
    
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    gen treated = 0
    replace treated = 1 if city == "wi"
    


    def genTimeOfDay():
        #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
        
        gen morning = 0
        replace morning = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
        replace morning = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
        replace morning = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

        replace morning = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
        replace morning = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
        replace morning = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
        replace morning = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

        replace morning = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
        replace morning = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
        replace morning = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

        replace morning = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
        replace morning = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
        replace morning = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
        replace morning = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

        replace morning = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
        replace morning = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
        replace morning = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

        replace morning = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
        replace morning = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
        replace morning = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
        replace morning = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12


        gen earlymorning = 0
        replace earlymorning = 1 if city == "wi" & date <= 85 & hour <= 6
        replace earlymorning = 1 if city == "wi" & date > 85 & date <= 127 & hour <= 7
        replace earlymorning = 1 if city == "wi" & date > 127 & date <= 154 & hour <= 6

        replace earlymorning = 1 if city == "ct" & date <= 45 & hour <= 6
        replace earlymorning = 1 if city == "ct" & date > 45 & date <= 122 & hour <= 7
        replace earlymorning = 1 if city == "ct" & date > 122 & date <= 127 & hour <= 8
        replace earlymorning = 1 if city == "ct" & date > 127 & date <= 154 & hour <= 7

        replace earlymorning = 1 if city == "cl" & date <= 72 & hour <= 6
        replace earlymorning = 1 if city == "cl" & date > 72 & date <= 127 & hour <= 7
        replace earlymorning = 1 if city == "cl" & date > 127 & date <= 154 & hour <= 6

        replace earlymorning = 1 if city == "kn" & date <= 54 & hour <= 6
        replace earlymorning = 1 if city == "kn" & date > 54 & date <= 126 & hour <= 7
        replace earlymorning = 1 if city == "kn" & date > 126 & date <= 127 & hour <= 8
        replace earlymorning = 1 if city == "kn" & date > 127 & date <= 154 & hour <= 7

        replace earlymorning = 1 if city == "sa" & date <= 64 & hour <= 6
        replace earlymorning = 1 if city == "sa" & date > 64 & date <= 127 & hour <= 7
        replace earlymorning = 1 if city == "sa" & date > 127 & date <= 154 & hour <= 6

        replace earlymorning = 1 if city == "ne" & date <= 18 & hour <= 5
        replace earlymorning = 1 if city == "ne" & date > 18 & date <= 92 & hour <= 6
        replace earlymorning = 1 if city == "ne" & date > 92 & date <= 127 & hour <= 7
        replace earlymorning = 1 if city == "ne" & date > 127 & date <= 154 & hour <= 6



        gen afternoon = 0
        replace afternoon = 1 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
        replace afternoon = 1 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


        gen night = 0
        replace night = 1 if city == "wi" & date <= 45 & hour >= 20 
        replace night = 1 if city == "wi" & date > 45 & date <= 91 & hour >= 19 
        replace night = 1 if city == "wi" & date > 91 & date <= 127 & hour >= 18 
        replace night = 1 if city == "wi" & date > 127 & date <= 154 & hour >= 17 

        replace night = 1 if city == "ct" & date <= 69 & hour >= 20 
        replace night = 1 if city == "ct" & date > 69 & date <= 113 & hour >= 19 
        replace night = 1 if city == "ct" & date > 113 & date <= 127 & hour >= 18 
        replace night = 1 if city == "ct" & date > 127 & date <= 154 & hour >= 17 

        replace night = 1 if city == "cl" & date <= 51 & hour >= 20 
        replace night = 1 if city == "cl" & date > 51 & date <= 97 & hour >= 19 
        replace night = 1 if city == "cl" & date > 97 & date <= 127 & hour >= 18 
        replace night = 1 if city == "cl" & date > 127 & date <= 154 & hour >= 17 

        replace night = 1 if city == "kn" & date <= 66 & hour >= 20 
        replace night = 1 if city == "kn" & date > 66 & date <= 107 & hour >= 19 
        replace night = 1 if city == "kn" & date > 107 & date <= 127 & hour >= 18 
        replace night = 1 if city == "kn" & date > 127 & date <= 154 & hour >= 17 

        replace night = 1 if city == "sa" & date <= 54 & hour >= 20 
        replace night = 1 if city == "sa" & date > 54 & date <= 101 & hour >= 19 
        replace night = 1 if city == "sa" & date > 101 & date <= 127 & hour >= 18 
        replace night = 1 if city == "sa" & date > 127 & date <= 154 & hour >= 17 

        replace night = 1 if city == "ne" & date <= 44 & hour >= 20 
        replace night = 1 if city == "ne" & date > 44 & date <= 86 & hour >= 19 
        replace night = 1 if city == "ne" & date > 86 & date <= 127 & hour >= 18 
        replace night = 1 if city == "ne" & date > 127 & date <= 133 & hour >= 17 
        replace night = 1 if city == "ne" & date > 133 & date <= 154 & hour >= 16 

    ###

    def genDayOfWeek():
        gen weekend = 0
        replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

    ###    


    drop city eduhighbelow fulltimeemploymentrate vehiclenumberoccupied 
    # drop placeid nearestdist blockfips

    psmatch2 treated i.hour i.date speed_avg speed_max familysize incomemedian familymarriedhaskidrate raceblackrate fulltimeemploymentrate yearbuiltmedian plumbingcompleterate commutetime povertybelowrate, noreplace
    psmatch2 treated post earlymorning morning afternoon weekend incomemedian raceblackrate yearbuiltmedian commutetime povertybelowrate, noreplace
    save "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_psm.dta", replace






    
    preserve
    drop if (_weight ==.) & (treated == 0)
    
    drop if _weight ==.
    
    keep if post == 0
    ttest togetherb_avg, by(treated)
    ttest athomeavg, by(treated)
    ttest dist_home_avg, by(treated)
    ttest speed_avg, by(treated)
    ttest speed_max, by(treated)
    ttest familysize, by(treated)
    ttest incomemedian, by(treated)
    ttest familymarriedhaskidrate, by(treated)
    ttest raceblackrate, by(treated)
    ttest yearbuiltmedian, by(treated)
    ttest plumbingcompleterate, by(treated)
    ttest commutetime, by(treated)
    ttest povertybelowrate, by(treated)






def overtimeByPartial_mechanism_athomeToD()

    # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta"
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop dist_home_avg blockfips
    drop speed_avg speed_max
    # drop athomeavg
    drop familysize
    drop togetherb_avg


    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen partialTreated = 0
    replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"




def python_plot_totallyathome():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    keep if athomeavg == 1
    drop hour speed_avg speed_max familysize athomeavg  blockfips advertiser_id dist_home_avg
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    
    gen group = .
    replace group = 2 if city == "wi"
    replace group = 1 if city == "cl" | city == "ct" | city == "kn"
    replace group = 0 if city == "sa" | city == "ne"
    
    
    gen weeknumber = .
    replace weeknumber = 26 if date == 1
    replace weeknumber = 27 if date >= 2 & date <= 8
    replace weeknumber = 28 if date >= 9 & date <= 15
    replace weeknumber = 29 if date >= 16 & date <= 22
    replace weeknumber = 30 if date >= 23 & date <= 29
    replace weeknumber = 31 if date >= 30 & date <= 36
    replace weeknumber = 32 if date >= 37 & date <= 43
    replace weeknumber = 33 if date >= 44 & date <= 50
    replace weeknumber = 34 if date >= 51 & date <= 57
    replace weeknumber = 35 if date >= 58 & date <= 64
    replace weeknumber = 36 if date >= 65 & date <= 71
    replace weeknumber = 37 if date >= 72 & date <= 78
    replace weeknumber = 38 if date >= 79 & date <= 85
    replace weeknumber = 39 if date >= 86 & date <= 92
    replace weeknumber = 40 if date >= 93 & date <= 99
    replace weeknumber = 41 if date >= 100 & date <= 106
    replace weeknumber = 42 if date >= 107 & date <= 113
    replace weeknumber = 43 if date >= 114 & date <= 120
    replace weeknumber = 44 if date >= 121 & date <= 127
    replace weeknumber = 45 if date >= 128 & date <= 134
    replace weeknumber = 46 if date >= 135 & date <= 141
    replace weeknumber = 47 if date >= 142 & date <= 148
    replace weeknumber = 48 if date >= 149 & date <= 154
    
    drop post 
    
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 1, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    mean togetherb_avg if city == "wi", over(weeknumber)
    mean togetherb_avg if city == "cl", over(weeknumber)
    mean togetherb_avg if city == "ct", over(weeknumber)
    mean togetherb_avg if city == "kn", over(weeknumber)
    mean togetherb_avg if city == "sa", over(weeknumber)
    mean togetherb_avg if city == "ne", over(weeknumber)




def python_plot_outhome():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    keep if athomeavg == 0
    drop hour speed_avg speed_max familysize athomeavg blockfips advertiser_id dist_home_avg
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    
    gen group = .
    replace group = 2 if city == "wi"
    replace group = 1 if city == "cl" | city == "ct" | city == "kn"
    replace group = 0 if city == "sa" | city == "ne"
    
    
    gen weeknumber = .
    replace weeknumber = 26 if date == 1
    replace weeknumber = 27 if date >= 2 & date <= 8
    replace weeknumber = 28 if date >= 9 & date <= 15
    replace weeknumber = 29 if date >= 16 & date <= 22
    replace weeknumber = 30 if date >= 23 & date <= 29
    replace weeknumber = 31 if date >= 30 & date <= 36
    replace weeknumber = 32 if date >= 37 & date <= 43
    replace weeknumber = 33 if date >= 44 & date <= 50
    replace weeknumber = 34 if date >= 51 & date <= 57
    replace weeknumber = 35 if date >= 58 & date <= 64
    replace weeknumber = 36 if date >= 65 & date <= 71
    replace weeknumber = 37 if date >= 72 & date <= 78
    replace weeknumber = 38 if date >= 79 & date <= 85
    replace weeknumber = 39 if date >= 86 & date <= 92
    replace weeknumber = 40 if date >= 93 & date <= 99
    replace weeknumber = 41 if date >= 100 & date <= 106
    replace weeknumber = 42 if date >= 107 & date <= 113
    replace weeknumber = 43 if date >= 114 & date <= 120
    replace weeknumber = 44 if date >= 121 & date <= 127
    replace weeknumber = 45 if date >= 128 & date <= 134
    replace weeknumber = 46 if date >= 135 & date <= 141
    replace weeknumber = 47 if date >= 142 & date <= 148
    replace weeknumber = 48 if date >= 149 & date <= 154
    
    drop post 
    
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 1, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    mean togetherb_avg if city == "wi", over(weeknumber)
    mean togetherb_avg if city == "cl", over(weeknumber)
    mean togetherb_avg if city == "ct", over(weeknumber)
    mean togetherb_avg if city == "kn", over(weeknumber)
    mean togetherb_avg if city == "sa", over(weeknumber)
    mean togetherb_avg if city == "ne", over(weeknumber)



def python_plot_earlymorning():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop dist_home_avg blockfips
    drop speed_avg speed_max
    drop familysize

    drop athomeavg
    
    
    def genTimeOfDay():
        #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
        
        gen tod = .
        replace tod = 0 if city == "wi" & date <= 85 & hour <= 6
        replace tod = 0 if city == "wi" & date > 85 & date <= 127 & hour <= 7
        replace tod = 0 if city == "wi" & date > 127 & date <= 154 & hour <= 6

        replace tod = 0 if city == "ct" & date <= 45 & hour <= 6
        replace tod = 0 if city == "ct" & date > 45 & date <= 122 & hour <= 7
        replace tod = 0 if city == "ct" & date > 122 & date <= 127 & hour <= 8
        replace tod = 0 if city == "ct" & date > 127 & date <= 154 & hour <= 7

        replace tod = 0 if city == "cl" & date <= 72 & hour <= 6
        replace tod = 0 if city == "cl" & date > 72 & date <= 127 & hour <= 7
        replace tod = 0 if city == "cl" & date > 127 & date <= 154 & hour <= 6

        replace tod = 0 if city == "kn" & date <= 54 & hour <= 6
        replace tod = 0 if city == "kn" & date > 54 & date <= 126 & hour <= 7
        replace tod = 0 if city == "kn" & date > 126 & date <= 127 & hour <= 8
        replace tod = 0 if city == "kn" & date > 127 & date <= 154 & hour <= 7

        replace tod = 0 if city == "sa" & date <= 64 & hour <= 6
        replace tod = 0 if city == "sa" & date > 64 & date <= 127 & hour <= 7
        replace tod = 0 if city == "sa" & date > 127 & date <= 154 & hour <= 6

        replace tod = 0 if city == "ne" & date <= 18 & hour <= 5
        replace tod = 0 if city == "ne" & date > 18 & date <= 92 & hour <= 6
        replace tod = 0 if city == "ne" & date > 92 & date <= 127 & hour <= 7
        replace tod = 0 if city == "ne" & date > 127 & date <= 154 & hour <= 6

    ###
    
    keep if tod == 0
    drop tod
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    gen group = .
    replace group = 2 if city == "wi"
    replace group = 1 if city == "cl" | city == "ct" | city == "kn"
    replace group = 0 if city == "sa" | city == "ne"
    
    
    gen weeknumber = .
    replace weeknumber = 26 if date == 1
    replace weeknumber = 27 if date >= 2 & date <= 8
    replace weeknumber = 28 if date >= 9 & date <= 15
    replace weeknumber = 29 if date >= 16 & date <= 22
    replace weeknumber = 30 if date >= 23 & date <= 29
    replace weeknumber = 31 if date >= 30 & date <= 36
    replace weeknumber = 32 if date >= 37 & date <= 43
    replace weeknumber = 33 if date >= 44 & date <= 50
    replace weeknumber = 34 if date >= 51 & date <= 57
    replace weeknumber = 35 if date >= 58 & date <= 64
    replace weeknumber = 36 if date >= 65 & date <= 71
    replace weeknumber = 37 if date >= 72 & date <= 78
    replace weeknumber = 38 if date >= 79 & date <= 85
    replace weeknumber = 39 if date >= 86 & date <= 92
    replace weeknumber = 40 if date >= 93 & date <= 99
    replace weeknumber = 41 if date >= 100 & date <= 106
    replace weeknumber = 42 if date >= 107 & date <= 113
    replace weeknumber = 43 if date >= 114 & date <= 120
    replace weeknumber = 44 if date >= 121 & date <= 127
    replace weeknumber = 45 if date >= 128 & date <= 134
    replace weeknumber = 46 if date >= 135 & date <= 141
    replace weeknumber = 47 if date >= 142 & date <= 148
    replace weeknumber = 48 if date >= 149 & date <= 154
    
    drop post 
    
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 1, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    mean togetherb_avg if city == "wi", over(weeknumber)
    mean togetherb_avg if city == "cl", over(weeknumber)
    mean togetherb_avg if city == "ct", over(weeknumber)
    mean togetherb_avg if city == "kn", over(weeknumber)
    mean togetherb_avg if city == "sa", over(weeknumber)
    mean togetherb_avg if city == "ne", over(weeknumber)



def python_plot_morning():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop dist_home_avg blockfips
    drop speed_avg speed_max
    drop familysize

    drop athomeavg
    
    
    def genTimeOfDay():
        #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
        
        gen tod = .
        replace tod = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
        replace tod = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
        replace tod = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

        replace tod = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
        replace tod = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
        replace tod = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
        replace tod = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

        replace tod = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
        replace tod = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
        replace tod = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

        replace tod = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
        replace tod = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
        replace tod = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
        replace tod = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

        replace tod = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
        replace tod = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
        replace tod = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

        replace tod = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
        replace tod = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
        replace tod = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
        replace tod = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12



    ###
    keep if tod == 1
    drop tod
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    gen group = .
    replace group = 2 if city == "wi"
    replace group = 1 if city == "cl" | city == "ct" | city == "kn"
    replace group = 0 if city == "sa" | city == "ne"
    
    
    gen weeknumber = .
    replace weeknumber = 26 if date == 1
    replace weeknumber = 27 if date >= 2 & date <= 8
    replace weeknumber = 28 if date >= 9 & date <= 15
    replace weeknumber = 29 if date >= 16 & date <= 22
    replace weeknumber = 30 if date >= 23 & date <= 29
    replace weeknumber = 31 if date >= 30 & date <= 36
    replace weeknumber = 32 if date >= 37 & date <= 43
    replace weeknumber = 33 if date >= 44 & date <= 50
    replace weeknumber = 34 if date >= 51 & date <= 57
    replace weeknumber = 35 if date >= 58 & date <= 64
    replace weeknumber = 36 if date >= 65 & date <= 71
    replace weeknumber = 37 if date >= 72 & date <= 78
    replace weeknumber = 38 if date >= 79 & date <= 85
    replace weeknumber = 39 if date >= 86 & date <= 92
    replace weeknumber = 40 if date >= 93 & date <= 99
    replace weeknumber = 41 if date >= 100 & date <= 106
    replace weeknumber = 42 if date >= 107 & date <= 113
    replace weeknumber = 43 if date >= 114 & date <= 120
    replace weeknumber = 44 if date >= 121 & date <= 127
    replace weeknumber = 45 if date >= 128 & date <= 134
    replace weeknumber = 46 if date >= 135 & date <= 141
    replace weeknumber = 47 if date >= 142 & date <= 148
    replace weeknumber = 48 if date >= 149 & date <= 154
    
    drop post 
    
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 1, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    mean togetherb_avg if city == "wi", over(weeknumber)
    mean togetherb_avg if city == "cl", over(weeknumber)
    mean togetherb_avg if city == "ct", over(weeknumber)
    mean togetherb_avg if city == "kn", over(weeknumber)
    mean togetherb_avg if city == "sa", over(weeknumber)
    mean togetherb_avg if city == "ne", over(weeknumber)



def python_plot_afternoon():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop dist_home_avg blockfips
    drop speed_avg speed_max
    drop familysize

    drop athomeavg
    
    
    def genTimeOfDay():
        #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
        
        gen tod = .


        replace tod = 2 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
        replace tod = 2 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
        replace tod = 2 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
        replace tod = 2 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace tod = 2 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
        replace tod = 2 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
        replace tod = 2 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
        replace tod = 2 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace tod = 2 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
        replace tod = 2 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
        replace tod = 2 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
        replace tod = 2 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace tod = 2 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
        replace tod = 2 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
        replace tod = 2 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
        replace tod = 2 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace tod = 2 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
        replace tod = 2 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
        replace tod = 2 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
        replace tod = 2 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace tod = 2 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
        replace tod = 2 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
        replace tod = 2 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
        replace tod = 2 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
        replace tod = 2 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


    ###
    keep if tod == 2
    drop tod
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    gen group = .
    replace group = 2 if city == "wi"
    replace group = 1 if city == "cl" | city == "ct" | city == "kn"
    replace group = 0 if city == "sa" | city == "ne"
    
    
    gen weeknumber = .
    replace weeknumber = 26 if date == 1
    replace weeknumber = 27 if date >= 2 & date <= 8
    replace weeknumber = 28 if date >= 9 & date <= 15
    replace weeknumber = 29 if date >= 16 & date <= 22
    replace weeknumber = 30 if date >= 23 & date <= 29
    replace weeknumber = 31 if date >= 30 & date <= 36
    replace weeknumber = 32 if date >= 37 & date <= 43
    replace weeknumber = 33 if date >= 44 & date <= 50
    replace weeknumber = 34 if date >= 51 & date <= 57
    replace weeknumber = 35 if date >= 58 & date <= 64
    replace weeknumber = 36 if date >= 65 & date <= 71
    replace weeknumber = 37 if date >= 72 & date <= 78
    replace weeknumber = 38 if date >= 79 & date <= 85
    replace weeknumber = 39 if date >= 86 & date <= 92
    replace weeknumber = 40 if date >= 93 & date <= 99
    replace weeknumber = 41 if date >= 100 & date <= 106
    replace weeknumber = 42 if date >= 107 & date <= 113
    replace weeknumber = 43 if date >= 114 & date <= 120
    replace weeknumber = 44 if date >= 121 & date <= 127
    replace weeknumber = 45 if date >= 128 & date <= 134
    replace weeknumber = 46 if date >= 135 & date <= 141
    replace weeknumber = 47 if date >= 142 & date <= 148
    replace weeknumber = 48 if date >= 149 & date <= 154
    
    drop post 
    
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 1, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    mean togetherb_avg if city == "wi", over(weeknumber)
    mean togetherb_avg if city == "cl", over(weeknumber)
    mean togetherb_avg if city == "ct", over(weeknumber)
    mean togetherb_avg if city == "kn", over(weeknumber)
    mean togetherb_avg if city == "sa", over(weeknumber)
    mean togetherb_avg if city == "ne", over(weeknumber)



def python_plot_night():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop dist_home_avg blockfips
    drop speed_avg speed_max
    drop familysize

    drop athomeavg
    
    
    def genTimeOfDay():
        #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
        
        gen tod = .

        replace tod = 3 if city == "wi" & date <= 45 & hour >= 20 
        replace tod = 3 if city == "wi" & date > 45 & date <= 91 & hour >= 19 
        replace tod = 3 if city == "wi" & date > 91 & date <= 127 & hour >= 18 
        replace tod = 3 if city == "wi" & date > 127 & date <= 154 & hour >= 17 

        replace tod = 3 if city == "ct" & date <= 69 & hour >= 20 
        replace tod = 3 if city == "ct" & date > 69 & date <= 113 & hour >= 19 
        replace tod = 3 if city == "ct" & date > 113 & date <= 127 & hour >= 18 
        replace tod = 3 if city == "ct" & date > 127 & date <= 154 & hour >= 17 

        replace tod = 3 if city == "cl" & date <= 51 & hour >= 20 
        replace tod = 3 if city == "cl" & date > 51 & date <= 97 & hour >= 19 
        replace tod = 3 if city == "cl" & date > 97 & date <= 127 & hour >= 18 
        replace tod = 3 if city == "cl" & date > 127 & date <= 154 & hour >= 17 

        replace tod = 3 if city == "kn" & date <= 66 & hour >= 20 
        replace tod = 3 if city == "kn" & date > 66 & date <= 107 & hour >= 19 
        replace tod = 3 if city == "kn" & date > 107 & date <= 127 & hour >= 18 
        replace tod = 3 if city == "kn" & date > 127 & date <= 154 & hour >= 17 

        replace tod = 3 if city == "sa" & date <= 54 & hour >= 20 
        replace tod = 3 if city == "sa" & date > 54 & date <= 101 & hour >= 19 
        replace tod = 3 if city == "sa" & date > 101 & date <= 127 & hour >= 18 
        replace tod = 3 if city == "sa" & date > 127 & date <= 154 & hour >= 17 

        replace tod = 3 if city == "ne" & date <= 44 & hour >= 20 
        replace tod = 3 if city == "ne" & date > 44 & date <= 86 & hour >= 19 
        replace tod = 3 if city == "ne" & date > 86 & date <= 127 & hour >= 18 
        replace tod = 3 if city == "ne" & date > 127 & date <= 133 & hour >= 17 
        replace tod = 3 if city == "ne" & date > 133 & date <= 154 & hour >= 16 

    ###
    
    keep if tod == 3
    drop tod
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    gen group = .
    replace group = 2 if city == "wi"
    replace group = 1 if city == "cl" | city == "ct" | city == "kn"
    replace group = 0 if city == "sa" | city == "ne"
    
    
    gen weeknumber = .
    replace weeknumber = 26 if date == 1
    replace weeknumber = 27 if date >= 2 & date <= 8
    replace weeknumber = 28 if date >= 9 & date <= 15
    replace weeknumber = 29 if date >= 16 & date <= 22
    replace weeknumber = 30 if date >= 23 & date <= 29
    replace weeknumber = 31 if date >= 30 & date <= 36
    replace weeknumber = 32 if date >= 37 & date <= 43
    replace weeknumber = 33 if date >= 44 & date <= 50
    replace weeknumber = 34 if date >= 51 & date <= 57
    replace weeknumber = 35 if date >= 58 & date <= 64
    replace weeknumber = 36 if date >= 65 & date <= 71
    replace weeknumber = 37 if date >= 72 & date <= 78
    replace weeknumber = 38 if date >= 79 & date <= 85
    replace weeknumber = 39 if date >= 86 & date <= 92
    replace weeknumber = 40 if date >= 93 & date <= 99
    replace weeknumber = 41 if date >= 100 & date <= 106
    replace weeknumber = 42 if date >= 107 & date <= 113
    replace weeknumber = 43 if date >= 114 & date <= 120
    replace weeknumber = 44 if date >= 121 & date <= 127
    replace weeknumber = 45 if date >= 128 & date <= 134
    replace weeknumber = 46 if date >= 135 & date <= 141
    replace weeknumber = 47 if date >= 142 & date <= 148
    replace weeknumber = 48 if date >= 149 & date <= 154
    
    drop post 
    
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 1, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    mean togetherb_avg if city == "wi", over(weeknumber)
    mean togetherb_avg if city == "cl", over(weeknumber)
    mean togetherb_avg if city == "ct", over(weeknumber)
    mean togetherb_avg if city == "kn", over(weeknumber)
    mean togetherb_avg if city == "sa", over(weeknumber)
    mean togetherb_avg if city == "ne", over(weeknumber)



def python_plot_weekday():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop dist_home_avg blockfips
    drop speed_avg speed_max
    drop familysize

    drop athomeavg
    
    
    def genDayOfWeek():
        gen weekend = 0
        replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

    ###    
    
    keep if weekend == 0
    drop weekend
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    
    gen group = .
    replace group = 2 if city == "wi"
    replace group = 1 if city == "cl" | city == "ct" | city == "kn"
    replace group = 0 if city == "sa" | city == "ne"
    
    
    gen weeknumber = .
    replace weeknumber = 26 if date == 1
    replace weeknumber = 27 if date >= 2 & date <= 8
    replace weeknumber = 28 if date >= 9 & date <= 15
    replace weeknumber = 29 if date >= 16 & date <= 22
    replace weeknumber = 30 if date >= 23 & date <= 29
    replace weeknumber = 31 if date >= 30 & date <= 36
    replace weeknumber = 32 if date >= 37 & date <= 43
    replace weeknumber = 33 if date >= 44 & date <= 50
    replace weeknumber = 34 if date >= 51 & date <= 57
    replace weeknumber = 35 if date >= 58 & date <= 64
    replace weeknumber = 36 if date >= 65 & date <= 71
    replace weeknumber = 37 if date >= 72 & date <= 78
    replace weeknumber = 38 if date >= 79 & date <= 85
    replace weeknumber = 39 if date >= 86 & date <= 92
    replace weeknumber = 40 if date >= 93 & date <= 99
    replace weeknumber = 41 if date >= 100 & date <= 106
    replace weeknumber = 42 if date >= 107 & date <= 113
    replace weeknumber = 43 if date >= 114 & date <= 120
    replace weeknumber = 44 if date >= 121 & date <= 127
    replace weeknumber = 45 if date >= 128 & date <= 134
    replace weeknumber = 46 if date >= 135 & date <= 141
    replace weeknumber = 47 if date >= 142 & date <= 148
    replace weeknumber = 48 if date >= 149 & date <= 154
    
    drop post 
    
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 1, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    mean togetherb_avg if city == "wi", over(weeknumber)
    mean togetherb_avg if city == "cl", over(weeknumber)
    mean togetherb_avg if city == "ct", over(weeknumber)
    mean togetherb_avg if city == "kn", over(weeknumber)
    mean togetherb_avg if city == "sa", over(weeknumber)
    mean togetherb_avg if city == "ne", over(weeknumber)



def python_plot_weekend():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop dist_home_avg blockfips
    drop speed_avg speed_max
    drop familysize

    drop athomeavg
    
    
    def genDayOfWeek():
        gen weekend = 0
        replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

    ###    
    
    keep if weekend == 1
    drop weekend
    
    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .

    
    
    gen group = .
    replace group = 2 if city == "wi"
    replace group = 1 if city == "cl" | city == "ct" | city == "kn"
    replace group = 0 if city == "sa" | city == "ne"
    
    
    gen weeknumber = .
    replace weeknumber = 26 if date == 1
    replace weeknumber = 27 if date >= 2 & date <= 8
    replace weeknumber = 28 if date >= 9 & date <= 15
    replace weeknumber = 29 if date >= 16 & date <= 22
    replace weeknumber = 30 if date >= 23 & date <= 29
    replace weeknumber = 31 if date >= 30 & date <= 36
    replace weeknumber = 32 if date >= 37 & date <= 43
    replace weeknumber = 33 if date >= 44 & date <= 50
    replace weeknumber = 34 if date >= 51 & date <= 57
    replace weeknumber = 35 if date >= 58 & date <= 64
    replace weeknumber = 36 if date >= 65 & date <= 71
    replace weeknumber = 37 if date >= 72 & date <= 78
    replace weeknumber = 38 if date >= 79 & date <= 85
    replace weeknumber = 39 if date >= 86 & date <= 92
    replace weeknumber = 40 if date >= 93 & date <= 99
    replace weeknumber = 41 if date >= 100 & date <= 106
    replace weeknumber = 42 if date >= 107 & date <= 113
    replace weeknumber = 43 if date >= 114 & date <= 120
    replace weeknumber = 44 if date >= 121 & date <= 127
    replace weeknumber = 45 if date >= 128 & date <= 134
    replace weeknumber = 46 if date >= 135 & date <= 141
    replace weeknumber = 47 if date >= 142 & date <= 148
    replace weeknumber = 48 if date >= 149 & date <= 154
    
    drop post 
    
    mean togetherb_avg if group == 0, over(weeknumber)
    mean togetherb_avg if group == 1, over(weeknumber)
    mean togetherb_avg if group == 2, over(weeknumber)
    mean togetherb_avg if city == "wi", over(weeknumber)
    mean togetherb_avg if city == "cl", over(weeknumber)
    mean togetherb_avg if city == "ct", over(weeknumber)
    mean togetherb_avg if city == "kn", over(weeknumber)
    mean togetherb_avg if city == "sa", over(weeknumber)
    mean togetherb_avg if city == "ne", over(weeknumber)





# short term vs long term
def overTimeEffect_totoallyathome():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
    keep if athomeavg == 1
    drop speed_avg speed_max familysize athomeavg blockfips dist_home_avg
    

    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen partialTreated = 0
    replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"


    gen treatedPost = post * treated
    #gen partialTreatedPost = post * partialTreated
    gen notTreatedPost = post * notTreated

    drop post treatedPost

    xtset advertiser_id


    
    

    preserve
    drop if date >= 77+7
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_totoallyathome.doc, replace ctitle('main-one week') dec(2)
    restore


    preserve
    drop if date >= 77+30
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_totoallyathome.doc, ctitle('main-one month') dec(2)
    restore



    # preserve
    # drop if date >= 77+60
    # xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    # outreg2 using overTimeEffect_totoallyathome.doc, ctitle('main-two month') dec(2)
    # restore


    preserve
    drop if (date < 77+30 & date >= 77)
    drop if date >= 77+60
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_totoallyathome.doc, ctitle('main-month 2nd') dec(2)
    restore


    preserve
    drop if (date < 77+60 & date >= 77)
    drop if date >= 77+90
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_totoallyathome.doc, ctitle('main-month 3rd') dec(2)
    restore




###


# short term vs long term
def overTimeEffect_outhome():
    keep if athomeavg == 0
    drop speed_avg speed_max familysize athomeavg blockfips dist_home_avg
    

    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen partialTreated = 0
    replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"


    gen treatedPost = post * treated
    #gen partialTreatedPost = post * partialTreated
    gen notTreatedPost = post * notTreated

    drop post treatedPost

    xtset advertiser_id


    preserve
    drop if date >= 77+7
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_outhome.doc, replace ctitle('main-one week') dec(2)
    restore


    preserve
    drop if date >= 77+30
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_outhome.doc, ctitle('main-one month') dec(2)
    restore



    preserve
    drop if date >= 77+60
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_outhome.doc, ctitle('main-two month') dec(2)
    restore


    preserve
    drop if (date < 77+30 & date >= 77)
    drop if date >= 77+60
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_outhome.doc, ctitle('main-month 2nd') dec(2)
    restore


    preserve
    drop if (date < 77+60 & date >= 77)
    drop if date >= 77+90
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_outhome.doc, ctitle('main-month 3rd') dec(2)
    restore





    preserve
    drop if (date < 77+7 & date >= 77)
    drop if date >= 77+14
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_outhome.doc, ctitle('week2') dec(2)
    restore


    preserve
    drop if (date < 77+14 & date >= 77)
    drop if date >= 77+21
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_outhome.doc, ctitle('week3') dec(2)
    restore


    preserve
    drop if (date < 77+21 & date >= 77)
    drop if date >= 77+28
    xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
    outreg2 using overTimeEffect_outhome.doc, ctitle('week4') dec(2)
    restore

###


def partiallyTreated_mechanism_HomeTime_interactions_overtime():
    def athome():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta"
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg > 0

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        drop post
        
        xtset advertiser_id


        

        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athome.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athome.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athome.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athome.doc, ctitle('main-month 3rd') dec(2)
        restore



    def totoallyAthome():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==1

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        drop post notTreated

        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__totallyathome.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__totallyathome.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__totallyathome.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__totallyathome.doc, ctitle('main-month 3rd') dec(2)
        restore

    def outhome():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==0

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        drop post notTreated
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__outhome.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__outhome.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__outhome.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__outhome.doc, ctitle('main-month 3rd') dec(2)
        restore

    def tod_earlymorning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 0 if city == "wi" & date <= 85 & hour <= 6
            replace tod = 0 if city == "wi" & date > 85 & date <= 127 & hour <= 7
            replace tod = 0 if city == "wi" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ct" & date <= 45 & hour <= 6
            replace tod = 0 if city == "ct" & date > 45 & date <= 122 & hour <= 7
            replace tod = 0 if city == "ct" & date > 122 & date <= 127 & hour <= 8
            replace tod = 0 if city == "ct" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "cl" & date <= 72 & hour <= 6
            replace tod = 0 if city == "cl" & date > 72 & date <= 127 & hour <= 7
            replace tod = 0 if city == "cl" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "kn" & date <= 54 & hour <= 6
            replace tod = 0 if city == "kn" & date > 54 & date <= 126 & hour <= 7
            replace tod = 0 if city == "kn" & date > 126 & date <= 127 & hour <= 8
            replace tod = 0 if city == "kn" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "sa" & date <= 64 & hour <= 6
            replace tod = 0 if city == "sa" & date > 64 & date <= 127 & hour <= 7
            replace tod = 0 if city == "sa" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ne" & date <= 18 & hour <= 5
            replace tod = 0 if city == "ne" & date > 18 & date <= 92 & hour <= 6
            replace tod = 0 if city == "ne" & date > 92 & date <= 127 & hour <= 7
            replace tod = 0 if city == "ne" & date > 127 & date <= 154 & hour <= 6

        ###
        
        keep if tod == 0
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city post notTreated
        
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__earlymorning.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__earlymorning.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__earlymorning.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__earlymorning.doc, ctitle('main-month 3rd') dec(2)
        restore


    def tod_morning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
            replace tod = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
            replace tod = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
            replace tod = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
            replace tod = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
            replace tod = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
            replace tod = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
            replace tod = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
            replace tod = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
            replace tod = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12



        ###
        keep if tod == 1
        drop tod

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city post notTreated
        
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__morning.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__morning.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__morning.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__morning.doc, ctitle('main-month 3rd') dec(2)
        restore




    def tod_afternoon():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .


            replace tod = 2 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
            replace tod = 2 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
            replace tod = 2 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
            replace tod = 2 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
            replace tod = 2 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
            replace tod = 2 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
            replace tod = 2 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
            replace tod = 2 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
            replace tod = 2 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
            replace tod = 2 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


        ###
        keep if tod == 2
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city post notTreated
        
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__afternoon.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__afternoon.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__afternoon.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__afternoon.doc, ctitle('main-month 3rd') dec(2)
        restore




    def tod_night():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .

            replace tod = 3 if city == "wi" & date <= 45 & hour >= 20 
            replace tod = 3 if city == "wi" & date > 45 & date <= 91 & hour >= 19 
            replace tod = 3 if city == "wi" & date > 91 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "wi" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ct" & date <= 69 & hour >= 20 
            replace tod = 3 if city == "ct" & date > 69 & date <= 113 & hour >= 19 
            replace tod = 3 if city == "ct" & date > 113 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ct" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "cl" & date <= 51 & hour >= 20 
            replace tod = 3 if city == "cl" & date > 51 & date <= 97 & hour >= 19 
            replace tod = 3 if city == "cl" & date > 97 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "cl" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "kn" & date <= 66 & hour >= 20 
            replace tod = 3 if city == "kn" & date > 66 & date <= 107 & hour >= 19 
            replace tod = 3 if city == "kn" & date > 107 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "kn" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "sa" & date <= 54 & hour >= 20 
            replace tod = 3 if city == "sa" & date > 54 & date <= 101 & hour >= 19 
            replace tod = 3 if city == "sa" & date > 101 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "sa" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ne" & date <= 44 & hour >= 20 
            replace tod = 3 if city == "ne" & date > 44 & date <= 86 & hour >= 19 
            replace tod = 3 if city == "ne" & date > 86 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ne" & date > 127 & date <= 133 & hour >= 17 
            replace tod = 3 if city == "ne" & date > 133 & date <= 154 & hour >= 16 

        ###
        
        keep if tod == 3
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city post notTreated
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__night.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__night.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__night.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__night.doc, ctitle('main-month 3rd') dec(2)
        restore



        


    def dow_weekday():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 0
        drop weekend
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"
        drop city

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        
        drop post notTreated
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__weekday.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__weekday.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__weekday.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__weekday.doc, ctitle('main-month 3rd') dec(2)
        restore



        

        

    def dow_weekend():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 1
        drop weekend
        
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city post notTreated
        
        drop post notTreated
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__weekend.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__weekend.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__weekend.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__weekend.doc, ctitle('main-month 3rd') dec(2)
        restore



        

        


    def athome_tod_earlymorning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg > 0
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 0 if city == "wi" & date <= 85 & hour <= 6
            replace tod = 0 if city == "wi" & date > 85 & date <= 127 & hour <= 7
            replace tod = 0 if city == "wi" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ct" & date <= 45 & hour <= 6
            replace tod = 0 if city == "ct" & date > 45 & date <= 122 & hour <= 7
            replace tod = 0 if city == "ct" & date > 122 & date <= 127 & hour <= 8
            replace tod = 0 if city == "ct" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "cl" & date <= 72 & hour <= 6
            replace tod = 0 if city == "cl" & date > 72 & date <= 127 & hour <= 7
            replace tod = 0 if city == "cl" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "kn" & date <= 54 & hour <= 6
            replace tod = 0 if city == "kn" & date > 54 & date <= 126 & hour <= 7
            replace tod = 0 if city == "kn" & date > 126 & date <= 127 & hour <= 8
            replace tod = 0 if city == "kn" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "sa" & date <= 64 & hour <= 6
            replace tod = 0 if city == "sa" & date > 64 & date <= 127 & hour <= 7
            replace tod = 0 if city == "sa" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ne" & date <= 18 & hour <= 5
            replace tod = 0 if city == "ne" & date > 18 & date <= 92 & hour <= 6
            replace tod = 0 if city == "ne" & date > 92 & date <= 127 & hour <= 7
            replace tod = 0 if city == "ne" & date > 127 & date <= 154 & hour <= 6

        ###
        
        keep if tod == 0
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeEarlymorning.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeEarlymorning.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeEarlymorning.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeEarlymorning.doc, ctitle('main-month 3rd') dec(2)
        restore



        



    def athome_tod_morning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg > 0
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
            replace tod = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
            replace tod = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
            replace tod = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
            replace tod = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
            replace tod = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
            replace tod = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
            replace tod = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
            replace tod = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
            replace tod = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12



        ###
        keep if tod == 1
        drop tod

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeMorning.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeMorning.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeMorning.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeMorning.doc, ctitle('main-month 3rd') dec(2)
        restore



        




    def athome_tod_afternoon():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg > 0
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .


            replace tod = 2 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
            replace tod = 2 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
            replace tod = 2 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
            replace tod = 2 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
            replace tod = 2 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
            replace tod = 2 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
            replace tod = 2 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
            replace tod = 2 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
            replace tod = 2 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
            replace tod = 2 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


        ###
        keep if tod == 2
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeAfternoon.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeAfternoon.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeAfternoon.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeAfternoon.doc, ctitle('main-month 3rd') dec(2)
        restore



        




    def athome_tod_night():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg > 0
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .

            replace tod = 3 if city == "wi" & date <= 45 & hour >= 20 
            replace tod = 3 if city == "wi" & date > 45 & date <= 91 & hour >= 19 
            replace tod = 3 if city == "wi" & date > 91 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "wi" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ct" & date <= 69 & hour >= 20 
            replace tod = 3 if city == "ct" & date > 69 & date <= 113 & hour >= 19 
            replace tod = 3 if city == "ct" & date > 113 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ct" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "cl" & date <= 51 & hour >= 20 
            replace tod = 3 if city == "cl" & date > 51 & date <= 97 & hour >= 19 
            replace tod = 3 if city == "cl" & date > 97 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "cl" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "kn" & date <= 66 & hour >= 20 
            replace tod = 3 if city == "kn" & date > 66 & date <= 107 & hour >= 19 
            replace tod = 3 if city == "kn" & date > 107 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "kn" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "sa" & date <= 54 & hour >= 20 
            replace tod = 3 if city == "sa" & date > 54 & date <= 101 & hour >= 19 
            replace tod = 3 if city == "sa" & date > 101 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "sa" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ne" & date <= 44 & hour >= 20 
            replace tod = 3 if city == "ne" & date > 44 & date <= 86 & hour >= 19 
            replace tod = 3 if city == "ne" & date > 86 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ne" & date > 127 & date <= 133 & hour >= 17 
            replace tod = 3 if city == "ne" & date > 133 & date <= 154 & hour >= 16 

        ###
        
        keep if tod == 3
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        drop hour
        drop post notTreated
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeNight.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeNight.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeNight.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeNight.doc, ctitle('main-month 3rd') dec(2)
        restore



        



        


    def athome_dow_weekday():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg > 0
        drop athomeavg
        
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 0
        drop weekend
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id


        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeWeekday.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeWeekday.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeWeekday.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeWeekday.doc, ctitle('main-month 3rd') dec(2)
        restore



        



        
        

    def athome_dow_weekend():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg > 0
        drop athomeavg
        
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 1
        drop weekend
        
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id



        preserve
        drop if date >= 77+7
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeWeekend.doc, replace ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeWeekend.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeWeekend.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using partiallyTreated_mechanism_HomeTime_interactions_overtime__athomeWeekend.doc, ctitle('main-month 3rd') dec(2)
        restore



        


        


    def outhome_tod_earlymorning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==0
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 0 if city == "wi" & date <= 85 & hour <= 6
            replace tod = 0 if city == "wi" & date > 85 & date <= 127 & hour <= 7
            replace tod = 0 if city == "wi" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ct" & date <= 45 & hour <= 6
            replace tod = 0 if city == "ct" & date > 45 & date <= 122 & hour <= 7
            replace tod = 0 if city == "ct" & date > 122 & date <= 127 & hour <= 8
            replace tod = 0 if city == "ct" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "cl" & date <= 72 & hour <= 6
            replace tod = 0 if city == "cl" & date > 72 & date <= 127 & hour <= 7
            replace tod = 0 if city == "cl" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "kn" & date <= 54 & hour <= 6
            replace tod = 0 if city == "kn" & date > 54 & date <= 126 & hour <= 7
            replace tod = 0 if city == "kn" & date > 126 & date <= 127 & hour <= 8
            replace tod = 0 if city == "kn" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "sa" & date <= 64 & hour <= 6
            replace tod = 0 if city == "sa" & date > 64 & date <= 127 & hour <= 7
            replace tod = 0 if city == "sa" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ne" & date <= 18 & hour <= 5
            replace tod = 0 if city == "ne" & date > 18 & date <= 92 & hour <= 6
            replace tod = 0 if city == "ne" & date > 92 & date <= 127 & hour <= 7
            replace tod = 0 if city == "ne" & date > 127 & date <= 154 & hour <= 6

        ###
        
        keep if tod == 0
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_outhome_tod.doc, replace ctitle('outhome earlymorning') dec(2)



    def outhome_tod_morning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==0
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
            replace tod = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
            replace tod = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
            replace tod = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
            replace tod = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
            replace tod = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
            replace tod = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
            replace tod = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
            replace tod = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
            replace tod = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12



        ###
        keep if tod == 1
        drop tod

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_outhome_tod.doc, ctitle('outhome morning') dec(2)



    def outhome_tod_afternoon():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==0
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .


            replace tod = 2 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
            replace tod = 2 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
            replace tod = 2 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
            replace tod = 2 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
            replace tod = 2 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
            replace tod = 2 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
            replace tod = 2 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
            replace tod = 2 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
            replace tod = 2 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
            replace tod = 2 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


        ###
        keep if tod == 2
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_outhome_tod.doc, ctitle('outhome afternoon') dec(2)


    def outhome_tod_night():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==0
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .

            replace tod = 3 if city == "wi" & date <= 45 & hour >= 20 
            replace tod = 3 if city == "wi" & date > 45 & date <= 91 & hour >= 19 
            replace tod = 3 if city == "wi" & date > 91 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "wi" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ct" & date <= 69 & hour >= 20 
            replace tod = 3 if city == "ct" & date > 69 & date <= 113 & hour >= 19 
            replace tod = 3 if city == "ct" & date > 113 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ct" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "cl" & date <= 51 & hour >= 20 
            replace tod = 3 if city == "cl" & date > 51 & date <= 97 & hour >= 19 
            replace tod = 3 if city == "cl" & date > 97 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "cl" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "kn" & date <= 66 & hour >= 20 
            replace tod = 3 if city == "kn" & date > 66 & date <= 107 & hour >= 19 
            replace tod = 3 if city == "kn" & date > 107 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "kn" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "sa" & date <= 54 & hour >= 20 
            replace tod = 3 if city == "sa" & date > 54 & date <= 101 & hour >= 19 
            replace tod = 3 if city == "sa" & date > 101 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "sa" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ne" & date <= 44 & hour >= 20 
            replace tod = 3 if city == "ne" & date > 44 & date <= 86 & hour >= 19 
            replace tod = 3 if city == "ne" & date > 86 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ne" & date > 127 & date <= 133 & hour >= 17 
            replace tod = 3 if city == "ne" & date > 133 & date <= 154 & hour >= 16 

        ###
        
        keep if tod == 3
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        drop hour
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_outhome_tod.doc, ctitle('outhome night') dec(2)

        


    def outhome_dow_weekday():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==0
        drop athomeavg
        
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 0
        drop weekend
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_outhome_dow.doc, replace ctitle('outhome weekday') dec(2)

        

    def outhome_dow_weekend():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==0
        drop athomeavg
        
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 1
        drop weekend
        
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_outhome_dow.doc, ctitle('outhome weekend') dec(2)

        


    def totallyathome_tod_earlymorning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==1
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 0 if city == "wi" & date <= 85 & hour <= 6
            replace tod = 0 if city == "wi" & date > 85 & date <= 127 & hour <= 7
            replace tod = 0 if city == "wi" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ct" & date <= 45 & hour <= 6
            replace tod = 0 if city == "ct" & date > 45 & date <= 122 & hour <= 7
            replace tod = 0 if city == "ct" & date > 122 & date <= 127 & hour <= 8
            replace tod = 0 if city == "ct" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "cl" & date <= 72 & hour <= 6
            replace tod = 0 if city == "cl" & date > 72 & date <= 127 & hour <= 7
            replace tod = 0 if city == "cl" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "kn" & date <= 54 & hour <= 6
            replace tod = 0 if city == "kn" & date > 54 & date <= 126 & hour <= 7
            replace tod = 0 if city == "kn" & date > 126 & date <= 127 & hour <= 8
            replace tod = 0 if city == "kn" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "sa" & date <= 64 & hour <= 6
            replace tod = 0 if city == "sa" & date > 64 & date <= 127 & hour <= 7
            replace tod = 0 if city == "sa" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ne" & date <= 18 & hour <= 5
            replace tod = 0 if city == "ne" & date > 18 & date <= 92 & hour <= 6
            replace tod = 0 if city == "ne" & date > 92 & date <= 127 & hour <= 7
            replace tod = 0 if city == "ne" & date > 127 & date <= 154 & hour <= 6

        ###
        
        keep if tod == 0
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_totoallyathome_tod.doc, replace ctitle('totallyathome earlymorning') dec(2)



    def totallyathome_tod_morning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==1
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
            replace tod = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
            replace tod = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
            replace tod = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
            replace tod = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
            replace tod = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
            replace tod = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
            replace tod = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
            replace tod = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
            replace tod = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12



        ###
        keep if tod == 1
        drop tod

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_totoallyathome_tod.doc, ctitle('totallyathome morning') dec(2)



    def totallyathome_tod_afternoon():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==1
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .


            replace tod = 2 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
            replace tod = 2 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
            replace tod = 2 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
            replace tod = 2 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
            replace tod = 2 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
            replace tod = 2 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
            replace tod = 2 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
            replace tod = 2 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
            replace tod = 2 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
            replace tod = 2 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


        ###
        keep if tod == 2
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_totoallyathome_tod.doc, ctitle('totallyathome afternoon') dec(2)


    def totallyathome_tod_night():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==1
        drop athomeavg
        
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .

            replace tod = 3 if city == "wi" & date <= 45 & hour >= 20 
            replace tod = 3 if city == "wi" & date > 45 & date <= 91 & hour >= 19 
            replace tod = 3 if city == "wi" & date > 91 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "wi" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ct" & date <= 69 & hour >= 20 
            replace tod = 3 if city == "ct" & date > 69 & date <= 113 & hour >= 19 
            replace tod = 3 if city == "ct" & date > 113 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ct" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "cl" & date <= 51 & hour >= 20 
            replace tod = 3 if city == "cl" & date > 51 & date <= 97 & hour >= 19 
            replace tod = 3 if city == "cl" & date > 97 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "cl" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "kn" & date <= 66 & hour >= 20 
            replace tod = 3 if city == "kn" & date > 66 & date <= 107 & hour >= 19 
            replace tod = 3 if city == "kn" & date > 107 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "kn" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "sa" & date <= 54 & hour >= 20 
            replace tod = 3 if city == "sa" & date > 54 & date <= 101 & hour >= 19 
            replace tod = 3 if city == "sa" & date > 101 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "sa" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ne" & date <= 44 & hour >= 20 
            replace tod = 3 if city == "ne" & date > 44 & date <= 86 & hour >= 19 
            replace tod = 3 if city == "ne" & date > 86 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ne" & date > 127 & date <= 133 & hour >= 17 
            replace tod = 3 if city == "ne" & date > 133 & date <= 154 & hour >= 16 

        ###
        
        keep if tod == 3
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        drop hour
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_totoallyathome_tod.doc, ctitle('totallyathome night') dec(2)

        


    def totallyathome_dow_weekday():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==1
        drop athomeavg
        
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 0
        drop weekend
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_totallyathome_dow.doc, replace ctitle('totallyathome weekday') dec(2)

        

    def totallyathome_dow_weekend():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        keep if athomeavg ==1
        drop athomeavg
        
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 1
        drop weekend
        
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_totallyathome_dow.doc, ctitle('totallyathome weekend') dec(2)

        




    def weekday_tod_earlymorning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 0
        drop weekend

        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 0 if city == "wi" & date <= 85 & hour <= 6
            replace tod = 0 if city == "wi" & date > 85 & date <= 127 & hour <= 7
            replace tod = 0 if city == "wi" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ct" & date <= 45 & hour <= 6
            replace tod = 0 if city == "ct" & date > 45 & date <= 122 & hour <= 7
            replace tod = 0 if city == "ct" & date > 122 & date <= 127 & hour <= 8
            replace tod = 0 if city == "ct" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "cl" & date <= 72 & hour <= 6
            replace tod = 0 if city == "cl" & date > 72 & date <= 127 & hour <= 7
            replace tod = 0 if city == "cl" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "kn" & date <= 54 & hour <= 6
            replace tod = 0 if city == "kn" & date > 54 & date <= 126 & hour <= 7
            replace tod = 0 if city == "kn" & date > 126 & date <= 127 & hour <= 8
            replace tod = 0 if city == "kn" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "sa" & date <= 64 & hour <= 6
            replace tod = 0 if city == "sa" & date > 64 & date <= 127 & hour <= 7
            replace tod = 0 if city == "sa" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ne" & date <= 18 & hour <= 5
            replace tod = 0 if city == "ne" & date > 18 & date <= 92 & hour <= 6
            replace tod = 0 if city == "ne" & date > 92 & date <= 127 & hour <= 7
            replace tod = 0 if city == "ne" & date > 127 & date <= 154 & hour <= 6

        ###
        
        keep if tod == 0
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_weekday_tod.doc, replace ctitle('weekday earlymorning') dec(2)



    def weekday_tod_morning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 0
        drop weekend
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
            replace tod = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
            replace tod = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
            replace tod = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
            replace tod = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
            replace tod = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
            replace tod = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
            replace tod = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
            replace tod = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
            replace tod = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12



        ###
        keep if tod == 1
        drop tod

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_weekday_tod.doc, ctitle('weekday morning') dec(2)



    def weekday_tod_afternoon():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 0
        drop weekend
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .


            replace tod = 2 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
            replace tod = 2 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
            replace tod = 2 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
            replace tod = 2 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
            replace tod = 2 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
            replace tod = 2 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
            replace tod = 2 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
            replace tod = 2 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
            replace tod = 2 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
            replace tod = 2 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


        ###
        keep if tod == 2
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_weekday_tod.doc, ctitle('weekday afternoon') dec(2)


    def weekday_tod_night():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 0
        drop weekend
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .

            replace tod = 3 if city == "wi" & date <= 45 & hour >= 20 
            replace tod = 3 if city == "wi" & date > 45 & date <= 91 & hour >= 19 
            replace tod = 3 if city == "wi" & date > 91 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "wi" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ct" & date <= 69 & hour >= 20 
            replace tod = 3 if city == "ct" & date > 69 & date <= 113 & hour >= 19 
            replace tod = 3 if city == "ct" & date > 113 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ct" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "cl" & date <= 51 & hour >= 20 
            replace tod = 3 if city == "cl" & date > 51 & date <= 97 & hour >= 19 
            replace tod = 3 if city == "cl" & date > 97 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "cl" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "kn" & date <= 66 & hour >= 20 
            replace tod = 3 if city == "kn" & date > 66 & date <= 107 & hour >= 19 
            replace tod = 3 if city == "kn" & date > 107 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "kn" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "sa" & date <= 54 & hour >= 20 
            replace tod = 3 if city == "sa" & date > 54 & date <= 101 & hour >= 19 
            replace tod = 3 if city == "sa" & date > 101 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "sa" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ne" & date <= 44 & hour >= 20 
            replace tod = 3 if city == "ne" & date > 44 & date <= 86 & hour >= 19 
            replace tod = 3 if city == "ne" & date > 86 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ne" & date > 127 & date <= 133 & hour >= 17 
            replace tod = 3 if city == "ne" & date > 133 & date <= 154 & hour >= 16 

        ###
        
        keep if tod == 3
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        drop hour
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_weekday_tod.doc, ctitle('weekday night') dec(2)

        



    def weekend_tod_earlymorning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 1
        drop weekend

        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 0 if city == "wi" & date <= 85 & hour <= 6
            replace tod = 0 if city == "wi" & date > 85 & date <= 127 & hour <= 7
            replace tod = 0 if city == "wi" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ct" & date <= 45 & hour <= 6
            replace tod = 0 if city == "ct" & date > 45 & date <= 122 & hour <= 7
            replace tod = 0 if city == "ct" & date > 122 & date <= 127 & hour <= 8
            replace tod = 0 if city == "ct" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "cl" & date <= 72 & hour <= 6
            replace tod = 0 if city == "cl" & date > 72 & date <= 127 & hour <= 7
            replace tod = 0 if city == "cl" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "kn" & date <= 54 & hour <= 6
            replace tod = 0 if city == "kn" & date > 54 & date <= 126 & hour <= 7
            replace tod = 0 if city == "kn" & date > 126 & date <= 127 & hour <= 8
            replace tod = 0 if city == "kn" & date > 127 & date <= 154 & hour <= 7

            replace tod = 0 if city == "sa" & date <= 64 & hour <= 6
            replace tod = 0 if city == "sa" & date > 64 & date <= 127 & hour <= 7
            replace tod = 0 if city == "sa" & date > 127 & date <= 154 & hour <= 6

            replace tod = 0 if city == "ne" & date <= 18 & hour <= 5
            replace tod = 0 if city == "ne" & date > 18 & date <= 92 & hour <= 6
            replace tod = 0 if city == "ne" & date > 92 & date <= 127 & hour <= 7
            replace tod = 0 if city == "ne" & date > 127 & date <= 154 & hour <= 6

        ###
        
        keep if tod == 0
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_weekend_tod.doc, replace ctitle('weekend earlymorning') dec(2)



    def weekend_tod_morning():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 1
        drop weekend
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .
            replace tod = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
            replace tod = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
            replace tod = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
            replace tod = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
            replace tod = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
            replace tod = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
            replace tod = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
            replace tod = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

            replace tod = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
            replace tod = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

            replace tod = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
            replace tod = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
            replace tod = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
            replace tod = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12



        ###
        keep if tod == 1
        drop tod

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_weekend_tod.doc, ctitle('weekend morning') dec(2)



    def weekday_tod_afternoon():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 1
        drop weekend
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .


            replace tod = 2 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
            replace tod = 2 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
            replace tod = 2 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
            replace tod = 2 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
            replace tod = 2 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
            replace tod = 2 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
            replace tod = 2 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
            replace tod = 2 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
            replace tod = 2 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

            replace tod = 2 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
            replace tod = 2 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
            replace tod = 2 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
            replace tod = 2 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
            replace tod = 2 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


        ###
        keep if tod == 2
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        drop hour
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_weekend_tod.doc, ctitle('weekend afternoon') dec(2)


    def weekday_tod_night():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        drop dist_home_avg blockfips
        drop speed_avg speed_max
        drop familysize

        drop athomeavg
        def genDayOfWeek():
            gen weekend = 0
            replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

        ###    
        
        keep if weekend == 1
        drop weekend
        
        def genTimeOfDay():
            #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018
            
            gen tod = .

            replace tod = 3 if city == "wi" & date <= 45 & hour >= 20 
            replace tod = 3 if city == "wi" & date > 45 & date <= 91 & hour >= 19 
            replace tod = 3 if city == "wi" & date > 91 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "wi" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ct" & date <= 69 & hour >= 20 
            replace tod = 3 if city == "ct" & date > 69 & date <= 113 & hour >= 19 
            replace tod = 3 if city == "ct" & date > 113 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ct" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "cl" & date <= 51 & hour >= 20 
            replace tod = 3 if city == "cl" & date > 51 & date <= 97 & hour >= 19 
            replace tod = 3 if city == "cl" & date > 97 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "cl" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "kn" & date <= 66 & hour >= 20 
            replace tod = 3 if city == "kn" & date > 66 & date <= 107 & hour >= 19 
            replace tod = 3 if city == "kn" & date > 107 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "kn" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "sa" & date <= 54 & hour >= 20 
            replace tod = 3 if city == "sa" & date > 54 & date <= 101 & hour >= 19 
            replace tod = 3 if city == "sa" & date > 101 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "sa" & date > 127 & date <= 154 & hour >= 17 

            replace tod = 3 if city == "ne" & date <= 44 & hour >= 20 
            replace tod = 3 if city == "ne" & date > 44 & date <= 86 & hour >= 19 
            replace tod = 3 if city == "ne" & date > 86 & date <= 127 & hour >= 18 
            replace tod = 3 if city == "ne" & date > 127 & date <= 133 & hour >= 17 
            replace tod = 3 if city == "ne" & date > 133 & date <= 154 & hour >= 16 

        ###
        
        keep if tod == 3
        drop tod
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        drop date
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        drop athomeavg
        drop city
        drop hour
        drop post notTreated
        xtset advertiser_id

        xtreg togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost, fe robust cluster(advertiser_id)
        test partialTreated == treatedPost  
        #p<0.01
        test notTreatedPost == treatedPost  
        #p<0.01
        test notTreatedPost == partialTreated  
        #p<0.01

        outreg2 using partiallyTreated_mechanism_weekend_tod.doc, ctitle('weekend night') dec(2)

        



def robust_binaryDVtogether():
    def main():
        # use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta"
        # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        use "H:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta",clear
        cd "H:\20181110_gpsHealth\process\v3\stataOut"

        drop dist_home_avg placeid nearestdist blockfips
        drop familysize speed_max speed_avg
        drop athomeavg

        # egen ncity = group(city)
        #tab ncity city
        #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
        #chattanooga, knoxville, and charleston were partially influenced. 
        #ne-1;sa-2;wi-3

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .
        
        gen togetherb_avg_B = .
        replace togetherb_avg_B = 0 if togetherb_avg == 0
        replace togetherb_avg_B = 1 if togetherb_avg > 0
        drop togetherb_avg
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        #gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        # gen togethorB = 0
        # replace togethorB = 1 if outtogethor > 0
        xtset advertiser_id

        drop if partialTreated == 1
        drop partialTreated
        logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
        # margins, dydx(post) at(treated=1) vsquish
        #dy/dx = .1693934, p<0.00
        outreg2 using report_tables9.doc, replace ctitle('main-noFE')



    ###


    ##this is for table 3 in 20201010
    def overTime_TC():
        preserve
        drop if date >= 77+7
        logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using report_tables10.doc, replace ctitle('main-one week-noFE')
        restore


        preserve
        drop if date >= 77+30
        logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using report_tables10.doc, ctitle('main-one month-noFE')
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using report_tables10.doc, ctitle('main-month 2nd-noFE')
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using report_tables10.doc, ctitle('main-month 3rd-noFE')
        restore


    ###




    ##########################partially treated
    def partially treated():

        def read_clean_data():
            # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
            # use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta"
            # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
            use "H:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
            cd "H:\20181110_gpsHealth\process\v3\stataOut"

            drop dist_home_avg blockfips
            drop speed_avg speed_max
            drop athomeavg
            drop familysize
            # egen ncity = group(city)
            # tab ncity city
            #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
            #chattanooga, knoxville, and charleston were partially influenced. 
            #ne-1;sa-2;wi-3
            
            gen post = 0 if date <= 75
            replace post = 1 if date >= 77
            drop if post == .
                    
            gen togetherb_avg_B = .
            replace togetherb_avg_B = 0 if togetherb_avg == 0
            replace togetherb_avg_B = 1 if togetherb_avg > 0
            drop togetherb_avg
            
            gen treated = 0
            replace treated = 1 if city == "wi"
            gen partialTreated = 0
            replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
            gen notTreated = 0
            replace notTreated = 1 if city == "sa" | city == "ne"

            gen treatedPost = post * treated
            gen partialTreatedPost = post * partialTreated
            gen notTreatedPost = post * notTreated

            
            drop notTreated
            
        ###

        xtset advertiser_id

        #main result
        logit togetherb_avg_B treated partialTreated post treatedPost partialTreatedPost i.hour, robust cluster(advertiser_id)
        #xtlogit athome treated notTreatedPost partialTreated treatedPost partialTreatedPost i.hour numspeeds_no0, robust cluster(advertiser_id)
        # test partialTreated == treatedPost  
        # #p<0.00
        # test notTreatedPost == treatedPost  
        # #p<0.00
        # test notTreatedPost == partialTreated  
        #p<0.00
        outreg2 using report_tables9.doc, ctitle('partial-main')



    # short term vs long term
    def overTimeEffect():
        preserve
        drop if date >= 77+7
        logit togetherb_avg_B treated partialTreated post treatedPost partialTreatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using report_tables10.doc, ctitle('main-one week')
        restore


        preserve
        drop if date >= 77+30
        logit togetherb_avg_B treated partialTreated post treatedPost partialTreatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using report_tables10.doc, ctitle('main-one month')
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        logit togetherb_avg_B treated partialTreated post treatedPost partialTreatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using report_tables10.doc, ctitle('main-month 2nd')
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        logit togetherb_avg_B treated partialTreated post treatedPost partialTreatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using report_tables10.doc, ctitle('main-month 3rd')
        restore


    ###





    #########################census block demographics moderating
    def mod_blcokData():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block.csv"
        # use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta"
        # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"

        use "H:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta",clear
        cd "H:\20181110_gpsHealth\process\v3\stataOut"

        drop dist_home_avg blockfips familymarriedhaskidrate athomeavg


        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen togetherb_avg_B = .
        replace togetherb_avg_B = 0 if togetherb_avg == 0
        replace togetherb_avg_B = 1 if togetherb_avg > 0
        drop togetherb_avg
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        #gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        # gen togethorB = 0
        # replace togethorB = 1 if outtogethor > 0
        drop city date
        xtset advertiser_id

        drop employmentcivilianrate    yearbuiltmedian  plumbingcompleterate commutetime  commutewalkrate povertybelowrate 
        drop maritaldrate vehiclenumberpercapita maritalwidowedrate
        drop vacancy4occasionalrate vacancy4salerate vacancy4rentrate
        drop familyhaskidrate raceblackrate eduhighbelowrate fulltimeemploymentrate employmentrate marriedspousepresentrate commutehomerate

        gen modIncomemedian = treatedPost * incomemedian
        gen postIncomemedian = post * incomemedian
        gen treatIncomemedian = treated * incomemedian
        logit togetherb_avg_B modIncomemedian incomemedian postIncomemedian treatIncomemedian post treatedPost i.hour treated, robust cluster(advertiser_id)
        outreg2 using report_tables11.doc, replace ctitle('modIncomeMedian')
        drop incomemedian modIncomemedian postIncomemedian treatIncomemedian


        gen modvacancyrate = treatedPost * vacancyrate
        gen postvacancyrate = post * vacancyrate
        gen treatvacancyrate = treated * vacancyrate
        logit togetherb_avg_B modvacancyrate vacancyrate postvacancyrate treatvacancyrate post treatedPost i.hour treated, robust cluster(advertiser_id)
        outreg2 using report_tables11.doc, ctitle('modvacancyrate')
        drop modvacancyrate vacancyrate postvacancyrate treatvacancyrate


        gen modcommutepublicrate = treatedPost * commutepublicrate
        gen postcommutepublicrate = post * commutepublicrate
        gen treatcommutepublicrate = treated * commutepublicrate
        logit togetherb_avg_B modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate post treatedPost i.hour treated, robust cluster(advertiser_id)
        outreg2 using report_tables11.doc, ctitle('modcommutepublicrate')
        drop modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate







def robustness_betaReg():
    def main():
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta"
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        use "H:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta",clear
        cd "H:\20181110_gpsHealth\process\v3\stataOut"

        drop dist_home_avg placeid nearestdist blockfips
        drop familysize speed_max speed_avg
        drop athomeavg

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .
        
        # gen newdv = (togetherb_avg *(36020422-1) + 0.5) / 36020422
        # gen newdv = (togetherb_avg *(3602042-1) + 0.5) / 3602042
        # drop togetherb_avg
        # gen togetherb_avg = newdv
        # drop newdv
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"
        egen ncity = group(city)
        #tab ncity city
        #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
        #chattanooga, knoxville, and charleston were partially influenced. 
        #ne-1;sa-2;wi-3


        gen treatedPost = post * treated
        #gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        # gen togethorB = 0
        # replace togethorB = 1 if outtogethor > 0

        drop if partialTreated == 1
        drop partialTreated
        fracreg logit togetherb_avg post treated treatedPost i.hour
        # margins, dydx(post) at(treated=1) vsquish   
        #dy/dx = .1693934, p<0.00
        outreg2 using robust_betaReg.doc, replace ctitle('main')

        drop advertiser_id notTreated notTreatedPost
        drop city
        fracreg logit togetherb_avg post treated treatedPost i.hour i.date i.ncity
        # margins, dydx(post) at(treated=1) vsquish   
        #dy/dx = , p<0.00
        outreg2 using robust_betaReg.doc, ctitle('main-control') dec(2)


    ###


    ##this is for table 3 in 20201010
    def overTime_TC():
        preserve
        drop if date >= 77+7
        fracreg logit togetherb_avg post treated treatedPost i.hour
        outreg2 using robust_betaReg.doc, ctitle('main-one week')
        restore


        preserve
        drop if date >= 77+30
        fracreg logit togetherb_avg post treated treatedPost i.hour
        outreg2 using robust_betaReg.doc, ctitle('main-one month')
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        fracreg logit togetherb_avg post treated treatedPost i.hour
        outreg2 using robust_betaReg.doc, ctitle('main-month 2nd')
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        fracreg logit togetherb_avg post treated treatedPost i.hour
        outreg2 using robust_betaReg.doc, ctitle('main-month 3rd')
        restore


    ###




    ##########################partially treated
    def partially treated():

        def read_clean_data():
            # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
            use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta", clear
            cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
            drop dist_home_avg blockfips
            drop speed_avg speed_max
            drop athomeavg
            drop familysize
            # egen ncity = group(city)
            # tab ncity city
            #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
            #chattanooga, knoxville, and charleston were partially influenced. 
            #ne-1;sa-2;wi-3
            
            gen post = 0 if date <= 75
            replace post = 1 if date >= 77
            drop if post == .
            
            # gen newdv = (togetherb_avg *(93631371-1) + 0.5) / 93631371
            # gen newdv = (togetherb_avg *(9363137-1) + 0.5) / 9363137
            # drop togetherb_avg
            # gen togetherb_avg = newdv
            # drop newdv
            
            gen treated = 0
            replace treated = 1 if city == "wi"
            gen partialTreated = 0
            replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
            gen notTreated = 0
            replace notTreated = 1 if city == "sa" | city == "ne"

            gen treatedPost = post * treated
            gen partialTreatedPost = post * partialTreated
            gen notTreatedPost = post * notTreated

            
            drop city date
            drop post notTreated
            
        ###


        #main result
        fracreg logit togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour
        #xtlogit athome treated notTreatedPost partialTreated treatedPost partialTreatedPost i.hour numspeeds_no0, robust cluster(advertiser_id)
        # test partialTreated == treatedPost  
        # #p<0.00
        # test notTreatedPost == treatedPost  
        # #p<0.00
        # test notTreatedPost == partialTreated  
        #p<0.00
        outreg2 using robust_betaReg_partial.doc, replace ctitle('partial-main')



    # short term vs long term
    def overTimeEffect():
        preserve
        drop if date >= 77+7
        fracreg logit togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour
        outreg2 using robust_betaReg_partial.doc, ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        fracreg logit togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour
        outreg2 using robust_betaReg_partial.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        fracreg logit togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour
        outreg2 using robust_betaReg_partial.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        fracreg logit togetherb_avg treated partialTreated notTreatedPost treatedPost partialTreatedPost i.hour
        outreg2 using robust_betaReg_partial.doc, ctitle('main-month 3rd') dec(2)
        restore


    ###





    #########################census block demographics moderating
    def mod_blcokData():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block.csv"
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta",clear
        cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"


        drop dist_home_avg blockfips familymarriedhaskidrate athomeavg


        # egen ncity = group(city)
        #tab ncity city
        #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
        #chattanooga, knoxville, and charleston were partially influenced. 
        #ne-1;sa-2;wi-3

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .
        
        # gen newdv = (togetherb_avg *(36020422-1) + 0.5) / 36020422
        # gen newdv = (togetherb_avg *(3602042-1) + 0.5) / 3602042
        # drop togetherb_avg
        # gen togetherb_avg = newdv
        # drop newdv
        
        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        #gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        # gen togethorB = 0
        # replace togethorB = 1 if outtogethor > 0
        drop city date

        drop employmentcivilianrate    yearbuiltmedian  plumbingcompleterate commutetime  commutewalkrate povertybelowrate 
        drop maritaldrate vehiclenumberpercapita maritalwidowedrate
        drop vacancy4occasionalrate vacancy4salerate vacancy4rentrate

        gen modIncomemedian = treatedPost * incomemedian
        gen postIncomemedian = post * incomemedian
        gen treatIncomemedian = treated * incomemedian
        fracreg logit togetherb_avg modIncomemedian incomemedian postIncomemedian treatIncomemedian post treated treatedPost i.hour
        outreg2 using robust_betaReg_blcokData.doc, replace ctitle('modIncomeMedian') dec(2)
        drop incomemedian modIncomemedian postIncomemedian treatIncomemedian
        
        
        # gen modRaceblackrate = treatedPost * raceblackrate
        # gen postRaceblackrate = post * raceblackrate
        # gen treatRaceblackrate = treated * raceblackrate
        # betareg togetherb_avg modRaceblackrate raceblackrate postRaceblackrate treatRaceblackrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        # outreg2 using robust_betaReg_blcokData.doc, ctitle('modRaceBlackRate') dec(2)
        # drop modRaceblackrate raceblackrate postRaceblackrate treatRaceblackrate
        
        # gen modmarriedspousepresentrate = treatedPost * marriedspousepresentrate
        # gen postmarriedspousepresentrate = post * marriedspousepresentrate
        # gen treatmarriedspousepresentrate = treated * marriedspousepresentrate
        # betareg togetherb_avg modmarriedspousepresentrate marriedspousepresentrate postmarriedspousepresentrate treatmarriedspousepresentrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        # outreg2 using robust_betaReg_blcokData.doc, ctitle('modmarriedspousepresentrate') dec(2)
        # drop modmarriedspousepresentrate marriedspousepresentrate postmarriedspousepresentrate treatmarriedspousepresentrate

        gen modvacancyrate = treatedPost * vacancyrate
        gen postvacancyrate = post * vacancyrate
        gen treatvacancyrate = treated * vacancyrate
        fracreg logit togetherb_avg modvacancyrate vacancyrate postvacancyrate treatvacancyrate post treated treatedPost i.hour
        outreg2 using robust_betaReg_blcokData.doc, ctitle('modvacancyrate') dec(2)
        drop modvacancyrate vacancyrate postvacancyrate treatvacancyrate


        gen modcommutepublicrate = treatedPost * commutepublicrate
        gen postcommutepublicrate = post * commutepublicrate
        gen treatcommutepublicrate = treated * commutepublicrate
        fracreg logit togetherb_avg modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate post treated treatedPost i.hour
        outreg2 using robust_betaReg_blcokData.doc, ctitle('modcommutepublicrate') dec(2)
        drop modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate

        # gen modvacancy4occasionalrate = treatedPost * vacancy4occasionalrate
        # gen postvacancy4occasionalrate = post * vacancy4occasionalrate
        # gen treatvacancy4occasionalrate = treated * vacancy4occasionalrate
        # betareg togetherb_avg modvacancy4occasionalrate vacancy4occasionalrate postvacancy4occasionalrate treatvacancy4occasionalrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        # outreg2 using robust_betaReg_blcokData.doc, ctitle('modvacancy4occasionalrate') dec(2)
        # drop modvacancy4occasionalrate vacancy4occasionalrate postvacancy4occasionalrate treatvacancy4occasionalrate


        # gen modvacancy4salerate = treatedPost * vacancy4salerate
        # gen postvacancy4salerate = post * vacancy4salerate
        # gen treatvacancy4salerate = treated * vacancy4salerate
        # betareg togetherb_avg modvacancy4salerate vacancy4salerate postvacancy4salerate treatvacancy4salerate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        # outreg2 using robust_betaReg_blcokData.doc, ctitle('modvacancy4salerate') dec(2)
        # drop modvacancy4salerate vacancy4salerate postvacancy4salerate treatvacancy4salerate


        # gen modvacancy4rentrate = treatedPost * vacancy4rentrate
        # gen postvacancy4rentrate = post * vacancy4rentrate
        # gen treatvacancy4rentrate = treated * vacancy4rentrate
        # betareg togetherb_avg modvacancy4rentrate vacancy4rentrate postvacancy4rentrate treatvacancy4rentrate post treated treatedPost i.hour, fe robust cluster(advertiser_id)
        # outreg2 using robust_betaReg_blcokData.doc, ctitle('modvacancy4rentrate') dec(2)
        # drop modvacancy4rentrate vacancy4rentrate postvacancy4rentrate treatvacancy4rentrate






def homedist_as_dv():
    # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.csv"
    # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        use "H:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta",clear
        cd "H:\20181110_gpsHealth\process\v3\stataOut"

    # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
    # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop placeid nearestdist blockfips speed_avg speed_max togetherb_avg athomeavg

    # egen ncity = group(city)
    #tab ncity city
    #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
    #chattanooga, knoxville, and charleston were partially influenced.
    #ne-1;sa-2;wi-3

    xtset advertiser_id

    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .

    gen treated = 0
    replace treated = 1 if city == "wi"
    gen partialTreated = 0
    replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
    gen notTreated = 0
    replace notTreated = 1 if city == "sa" | city == "ne"

    gen treatedPost = post * treated
    #gen partialTreatedPost = post * partialTreated
    gen notTreatedPost = post * notTreated
    # reg dist_home_avg post treated treatedPost i.hour, robust cluster(advertiser_id)
    # # margins, dydx(post) at(treated=1) vsquish   #dy/dx = .1693934, p<0.00
    # outreg2 using homedist_as_dv.doc, replace ctitle('main') dec(2)
    xtreg dist_home_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
    # margins, dydx(post) at(treated=1) vsquish   #dy/dx = .0785128, p<0.00
    #clogit athome post treated treatedPost i.hour numspeeds_no0, group(advertiser_id) robust cluster(advertiser_id)
    outreg2 using report_tables12_1.doc, replace ctitle('main-fe')



    def genTimeOfDay():
        #https://www.timeanddate.com/sun/usa/chattanooga?month=11&year=2018

        gen morning = 0
        replace morning = 1 if city == "wi" & date <= 85 & hour > 6 & hour < 12
        replace morning = 1 if city == "wi" & date > 85 & date <= 127 & hour > 7 & hour < 12
        replace morning = 1 if city == "wi" & date > 127 & date <= 154 & hour > 6 & hour < 12

        replace morning = 1 if city == "ct" & date <= 45 & hour > 6 & hour < 12
        replace morning = 1 if city == "ct" & date > 45 & date <= 122 & hour > 7 & hour < 12
        replace morning = 1 if city == "ct" & date > 122 & date <= 127 & hour > 8 & hour < 12
        replace morning = 1 if city == "ct" & date > 127 & date <= 154 & hour > 7 & hour < 12

        replace morning = 1 if city == "cl" & date <= 72 & hour > 6 & hour < 12
        replace morning = 1 if city == "cl" & date > 72 & date <= 127 & hour > 7 & hour < 12
        replace morning = 1 if city == "cl" & date > 127 & date <= 154 & hour > 6 & hour < 12

        replace morning = 1 if city == "kn" & date <= 54 & hour > 6 & hour < 12
        replace morning = 1 if city == "kn" & date > 54 & date <= 126 & hour > 7 & hour < 12
        replace morning = 1 if city == "kn" & date > 126 & date <= 127 & hour > 8 & hour < 12
        replace morning = 1 if city == "kn" & date > 127 & date <= 154 & hour > 7 & hour < 12

        replace morning = 1 if city == "sa" & date <= 64 & hour > 6 & hour < 12
        replace morning = 1 if city == "sa" & date > 64 & date <= 127 & hour > 7 & hour < 12
        replace morning = 1 if city == "sa" & date > 127 & date <= 154 & hour > 6 & hour < 12

        replace morning = 1 if city == "ne" & date <= 18 & hour > 5 & hour < 12
        replace morning = 1 if city == "ne" & date > 18 & date <= 92 & hour > 6 & hour < 12
        replace morning = 1 if city == "ne" & date > 92 & date <= 127 & hour > 7 & hour < 12
        replace morning = 1 if city == "ne" & date > 127 & date <= 154 & hour > 6 & hour < 12


        gen earlymorning = 0
        replace earlymorning = 1 if city == "wi" & date <= 85 & hour <= 6
        replace earlymorning = 1 if city == "wi" & date > 85 & date <= 127 & hour <= 7
        replace earlymorning = 1 if city == "wi" & date > 127 & date <= 154 & hour <= 6

        replace earlymorning = 1 if city == "ct" & date <= 45 & hour <= 6
        replace earlymorning = 1 if city == "ct" & date > 45 & date <= 122 & hour <= 7
        replace earlymorning = 1 if city == "ct" & date > 122 & date <= 127 & hour <= 8
        replace earlymorning = 1 if city == "ct" & date > 127 & date <= 154 & hour <= 7

        replace earlymorning = 1 if city == "cl" & date <= 72 & hour <= 6
        replace earlymorning = 1 if city == "cl" & date > 72 & date <= 127 & hour <= 7
        replace earlymorning = 1 if city == "cl" & date > 127 & date <= 154 & hour <= 6

        replace earlymorning = 1 if city == "kn" & date <= 54 & hour <= 6
        replace earlymorning = 1 if city == "kn" & date > 54 & date <= 126 & hour <= 7
        replace earlymorning = 1 if city == "kn" & date > 126 & date <= 127 & hour <= 8
        replace earlymorning = 1 if city == "kn" & date > 127 & date <= 154 & hour <= 7

        replace earlymorning = 1 if city == "sa" & date <= 64 & hour <= 6
        replace earlymorning = 1 if city == "sa" & date > 64 & date <= 127 & hour <= 7
        replace earlymorning = 1 if city == "sa" & date > 127 & date <= 154 & hour <= 6

        replace earlymorning = 1 if city == "ne" & date <= 18 & hour <= 5
        replace earlymorning = 1 if city == "ne" & date > 18 & date <= 92 & hour <= 6
        replace earlymorning = 1 if city == "ne" & date > 92 & date <= 127 & hour <= 7
        replace earlymorning = 1 if city == "ne" & date > 127 & date <= 154 & hour <= 6



        gen afternoon = 0
        replace afternoon = 1 if city == "wi" & date <= 45 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "wi" & date > 45 & date <= 91 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "wi" & date > 91 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "wi" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "ct" & date <= 69 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "ct" & date > 69 & date <= 113 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "ct" & date > 113 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "ct" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "cl" & date <= 51 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "cl" & date > 51 & date <= 97 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "cl" & date > 97 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "cl" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "kn" & date <= 66 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "kn" & date > 66 & date <= 107 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "kn" & date > 107 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "kn" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "sa" & date <= 54 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "sa" & date > 54 & date <= 101 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "sa" & date > 101 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "sa" & date > 127 & date <= 154 & hour < 17 & hour >= 12

        replace afternoon = 1 if city == "ne" & date <= 44 & hour < 20 & hour >= 12
        replace afternoon = 1 if city == "ne" & date > 44 & date <= 86 & hour < 19 & hour >= 12
        replace afternoon = 1 if city == "ne" & date > 86 & date <= 127 & hour < 18 & hour >= 12
        replace afternoon = 1 if city == "ne" & date > 127 & date <= 133 & hour < 17 & hour >= 12
        replace afternoon = 1 if city == "ne" & date > 133 & date <= 154 & hour < 16 & hour >= 12


        gen night = 0
        replace night = 1 if city == "wi" & date <= 45 & hour >= 20
        replace night = 1 if city == "wi" & date > 45 & date <= 91 & hour >= 19
        replace night = 1 if city == "wi" & date > 91 & date <= 127 & hour >= 18
        replace night = 1 if city == "wi" & date > 127 & date <= 154 & hour >= 17

        replace night = 1 if city == "ct" & date <= 69 & hour >= 20
        replace night = 1 if city == "ct" & date > 69 & date <= 113 & hour >= 19
        replace night = 1 if city == "ct" & date > 113 & date <= 127 & hour >= 18
        replace night = 1 if city == "ct" & date > 127 & date <= 154 & hour >= 17

        replace night = 1 if city == "cl" & date <= 51 & hour >= 20
        replace night = 1 if city == "cl" & date > 51 & date <= 97 & hour >= 19
        replace night = 1 if city == "cl" & date > 97 & date <= 127 & hour >= 18
        replace night = 1 if city == "cl" & date > 127 & date <= 154 & hour >= 17

        replace night = 1 if city == "kn" & date <= 66 & hour >= 20
        replace night = 1 if city == "kn" & date > 66 & date <= 107 & hour >= 19
        replace night = 1 if city == "kn" & date > 107 & date <= 127 & hour >= 18
        replace night = 1 if city == "kn" & date > 127 & date <= 154 & hour >= 17

        replace night = 1 if city == "sa" & date <= 54 & hour >= 20
        replace night = 1 if city == "sa" & date > 54 & date <= 101 & hour >= 19
        replace night = 1 if city == "sa" & date > 101 & date <= 127 & hour >= 18
        replace night = 1 if city == "sa" & date > 127 & date <= 154 & hour >= 17

        replace night = 1 if city == "ne" & date <= 44 & hour >= 20
        replace night = 1 if city == "ne" & date > 44 & date <= 86 & hour >= 19
        replace night = 1 if city == "ne" & date > 86 & date <= 127 & hour >= 18
        replace night = 1 if city == "ne" & date > 127 & date <= 133 & hour >= 17
        replace night = 1 if city == "ne" & date > 133 & date <= 154 & hour >= 16

    ###

    def genDayOfWeek():
        gen weekend = 0
        replace weekend = 1 if date==1 | date==2 | date==8 | date==9 | date==15 | date==16 | date==22 | date==23 | date==29 | date==30 | date==36 | date==37 | date==43 | date==44 | date==50 | date==51 | date==57 | date==58 | date==64 | date==65 | date==71 | date==72 | date==78 | date==79 | date==85 | date==86 | date==92 | date==93 | date==99 | date==100 | date==106 | date==107 | date==113 | date==114 | date==120 | date==121 | date==127 | date==128 | date==134 | date==135 | date==141 | date==142 | date==148 | date==149

    ###
    #
    # drop city
    # drop date




    gen modEarlymorning = treatedPost * earlymorning
    gen modMorning = treatedPost * morning
    gen modAfternoon = treatedPost * afternoon
    gen modNight = treatedPost * night

    gen postEarlymorning = post * earlymorning
    gen postMorning = post * morning
    gen postAfternoon = post * afternoon
    gen postNight = post * night

    gen treatedEarlymorning = treated * earlymorning
    gen treatedMorning = treated * morning
    gen treatedAfternoon = treated * afternoon
    gen treatedNight = treated * night
    xtreg dist_home_avg earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight postEarlymorning postMorning postAfternoon postNight treatedEarlymorning treatedMorning treatedAfternoon treatedNight post, fe robust cluster(advertiser_id)
    outreg2 using report_tables12_3.doc, replace ctitle('moderate-tod')

    gen modWeekend = treatedPost * weekend
    gen postWeekend = post * weekend
    gen treatedWeekend = treated * weekend
    xtreg dist_home_avg weekend modWeekend postWeekend treatedWeekend post treatedPost, fe robust cluster(advertiser_id)
    #xtlogit togethorB post treated earlymorning morning afternoon night modEarlymorning modMorning modAfternoon modNight numspeeds_no0, robust cluster(advertiser_id)
    outreg2 using report_tables12_3.doc, ctitle('moderate-weekend')


    # xtreg dist_home_avg post treated treatedPost i.hour i.date i.ncity, fe robust cluster(advertiser_id)
    # outreg2 using report_tables12_1.doc, ctitle('main-fe-control') dec(2)
    #
    #
    # xtreg dist_home_avg post treated treatedPost familysize i.hour i.date i.ncity, fe robust cluster(advertiser_id)
    # outreg2 using homedist_as_dv.doc, ctitle('main-fe-control-familysize') dec(2)


    def partial()
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.csv"
        # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        use "H:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        cd "H:\20181110_gpsHealth\process\v3\stataOut"
        drop blockfips
        drop speed_avg speed_max
        # drop athomeavg
        drop familysize

        # egen ncity = group(city)
        # tab ncity city
        #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
        #chattanooga, knoxville, and charleston were partially influenced.
        #ne-1;sa-2;wi-3

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated


        drop city
        # drop date dist_home maxspeeds avgspeeds_no0 city
        drop notTreated
        drop athomeavg togetherb_avg
        ###

        xtset advertiser_id
        xtreg dist_home_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        # test partialTreated == treatedPost
        # #p<0.0301
        # test notTreatedPost == treatedPost
        # #p<0.0016
        # test notTreatedPost == partialTreated
        #p<0.0467

        outreg2 using report_tables12_1.doc, ctitle('partial-main-fe')


    def overTime_TC():
        preserve
        drop if date >= 77+7
        xtreg dist_home_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_tables12_2.doc, ctitle('main-one week')
        restore


        preserve
        drop if date >= 77+30
        xtreg dist_home_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_tables12_2.doc, ctitle('main-one month')
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg dist_home_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_tables12_2.doc, ctitle('main-month 2nd')
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg dist_home_avg post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_tables12_2.doc, ctitle('main-month 3rd')
        restore


    def overTimeEffect():
        preserve
        drop if date >= 77+7
        xtreg dist_home_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        test treatedPost = partialTreatedPost
        outreg2 using report_tables12_2.doc, ctitle('main-one week')
        restore


        preserve
        drop if date >= 77+30
        xtreg dist_home_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        test treatedPost = partialTreatedPost   #0.0713
        outreg2 using report_tables12_2.doc, ctitle('main-one month')
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        xtreg dist_home_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        test treatedPost = partialTreatedPost
        outreg2 using report_tables12_2.doc, ctitle('main-month 2nd')
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        xtreg dist_home_avg post treatedPost partialTreatedPost i.hour, fe robust cluster(advertiser_id)
        test treatedPost = partialTreatedPost
        outreg2 using report_tables12_2.doc, ctitle('main-month 3rd')
        restore



    def mod_blcokData():
        # import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block.csv"
        # use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta"
        # cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
        use "H:\20181110_gpsHealth\process\v3\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_block_v1.dta",clear
        cd "H:\20181110_gpsHealth\process\v3\stataOut"


        drop blockfips familymarriedhaskidrate athomeavg


        # egen ncity = group(city)
        #tab ncity city
        #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
        #chattanooga, knoxville, and charleston were partially influenced.
        #ne-1;sa-2;wi-3

        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen treated = 0
        replace treated = 1 if city == "wi"
        gen partialTreated = 0
        replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
        gen notTreated = 0
        replace notTreated = 1 if city == "sa" | city == "ne"

        gen treatedPost = post * treated
        #gen partialTreatedPost = post * partialTreated
        gen notTreatedPost = post * notTreated

        # gen togethorB = 0
        # replace togethorB = 1 if outtogethor > 0
        drop city date

        drop employmentcivilianrate    yearbuiltmedian  plumbingcompleterate commutetime  commutewalkrate povertybelowrate
        drop maritaldrate vehiclenumberpercapita maritalwidowedrate
        drop vacancy4occasionalrate vacancy4salerate vacancy4rentrate
        drop togetherb_avg familyhaskidrate raceblackrate eduhighbelowrate fulltimeemploymentrate employmentrate marriedspousepresentrate commutehomerate

        xtset advertiser_id

        gen modIncomemedian = treatedPost * incomemedian
        gen postIncomemedian = post * incomemedian
        gen treatIncomemedian = treated * incomemedian
        xtreg dist_home_avg modIncomemedian incomemedian postIncomemedian treatIncomemedian post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_tables12_4.doc, ctitle('modIncomeMedian')
        drop incomemedian modIncomemedian postIncomemedian treatIncomemedian

        gen modvacancyrate = treatedPost * vacancyrate
        gen postvacancyrate = post * vacancyrate
        gen treatvacancyrate = treated * vacancyrate
        xtreg dist_home_avg modvacancyrate vacancyrate postvacancyrate treatvacancyrate post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_tables12_4.doc, ctitle('modvacancyrate')
        drop modvacancyrate vacancyrate postvacancyrate treatvacancyrate


        gen modcommutepublicrate = treatedPost * commutepublicrate
        gen postcommutepublicrate = post * commutepublicrate
        gen treatcommutepublicrate = treated * commutepublicrate
        xtreg dist_home_avg modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate post treatedPost i.hour, fe robust cluster(advertiser_id)
        outreg2 using report_tables12_4.doc, ctitle('modcommutepublicrate')
        drop modcommutepublicrate commutepublicrate postcommutepublicrate treatcommutepublicrate

###







    def python_plot():
        use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTPC.dta",clear
        drop hour speed_avg speed_max familysize athomeavg togetherb_avg blockfips advertiser_id
        gen post = 0 if date <= 75
        replace post = 1 if date >= 77
        drop if post == .

        gen group = .
        replace group = 2 if city == "wi"
        replace group = 1 if city == "cl" | city == "ct" | city == "kn"
        replace group = 0 if city == "sa" | city == "ne"


        gen weeknumber = .
        replace weeknumber = 26 if date == 1
        replace weeknumber = 27 if date >= 2 & date <= 8
        replace weeknumber = 28 if date >= 9 & date <= 15
        replace weeknumber = 29 if date >= 16 & date <= 22
        replace weeknumber = 30 if date >= 23 & date <= 29
        replace weeknumber = 31 if date >= 30 & date <= 36
        replace weeknumber = 32 if date >= 37 & date <= 43
        replace weeknumber = 33 if date >= 44 & date <= 50
        replace weeknumber = 34 if date >= 51 & date <= 57
        replace weeknumber = 35 if date >= 58 & date <= 64
        replace weeknumber = 36 if date >= 65 & date <= 71
        replace weeknumber = 37 if date >= 72 & date <= 78
        replace weeknumber = 38 if date >= 79 & date <= 85
        replace weeknumber = 39 if date >= 86 & date <= 92
        replace weeknumber = 40 if date >= 93 & date <= 99
        replace weeknumber = 41 if date >= 100 & date <= 106
        replace weeknumber = 42 if date >= 107 & date <= 113
        replace weeknumber = 43 if date >= 114 & date <= 120
        replace weeknumber = 44 if date >= 121 & date <= 127
        replace weeknumber = 45 if date >= 128 & date <= 134
        replace weeknumber = 46 if date >= 135 & date <= 141
        replace weeknumber = 47 if date >= 142 & date <= 148
        replace weeknumber = 48 if date >= 149 & date <= 154

        drop post

        mean dist_home_avg if group == 0, over(weeknumber)
        mean dist_home_avg if group == 1, over(weeknumber)
        mean dist_home_avg if group == 2, over(weeknumber)
        mean dist_home_avg if city == "wi", over(weeknumber)
        mean dist_home_avg if city == "cl", over(weeknumber)
        mean dist_home_avg if city == "ct", over(weeknumber)
        mean dist_home_avg if city == "kn", over(weeknumber)
        mean dist_home_avg if city == "sa", over(weeknumber)
        mean dist_home_avg if city == "ne", over(weeknumber)









######################matching

####use python to restructure data to user level
def matching():
    use "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\data\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC.dta"
    cd "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\result\stataOut"
    drop dist_home_avg placeid nearestdist blockfips
    drop familysize speed_max speed_avg
    drop athomeavg

    gen post = 0 if date <= 75
    replace post = 1 if date >= 77
    drop if post == .
    
    gen treated = 0
    replace treated = 1 if city == "wi"
    # gen partialTreated = 0
    # replace partialTreated = 1 if city == "cl" | city == "ct" | city == "kn"
    # gen notTreated = 0
    # replace notTreated = 1 if city == "sa" | city == "ne"


    keep if post == 0
    export delimited using "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\process\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_4matching.csv", replace
    
    
    def python_genUserLevel()
        import pandas as pd
        data = pd.read_csv('C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/process/s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_4matching.csv')
        data = data.groupby('advertiser_id').mean()
        data = data.reset_index(drop=False)
        data.to_csv('C:/Users/b2vec/Downloads/Family Bonding in Disruptive Natural Disaster/process/s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_4matching_python.csv',index=False)
    
    import delimited "C:\Users\b2vec\Downloads\Family Bonding in Disruptive Natural Disaster\process\s_07_11_both_valid10_abouthome_placeID_simpleid_familySize_hourly_together_blockID_merge_allcitiesTC_4matching_python.csv"
    drop if (treated != 0) & (treated != 1)
    psmatch2 treated hour date togetherb_avg, cal(.01)




    egen ncity = group(city)
    #tab ncity city
    #cl-1; ct-2; kn-3; ne-4;sa-5;wi-6
    #chattanooga, knoxville, and charleston were partially influenced. 
    #ne-1;sa-2;wi-3


    gen treatedPost = post * treated
    #gen partialTreatedPost = post * partialTreated
    gen notTreatedPost = post * notTreated

    # gen togethorB = 0
    # replace togethorB = 1 if outtogethor > 0

    drop if partialTreated == 1
    drop partialTreated
    logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
    margins, dydx(post) at(treated=1) vsquish   
    #dy/dx = .1693934, p<0.00
    outreg2 using robust_binaryDV.doc, replace ctitle('main') dec(2)

    logit togetherb_avg_B post treated treatedPost i.hour i.date i.ncity, robust cluster(advertiser_id)
    # margins, dydx(post) at(treated=1) vsquish   
    #dy/dx = , p<0.00
    outreg2 using robust_binaryDV.doc, ctitle('main-control') dec(2)


    ###


    ##this is for table 3 in 20201010
    def overTime_TC():
        preserve
        drop if date >= 77+7
        logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using robust_binaryDV.doc, ctitle('main-one week') dec(2)
        restore


        preserve
        drop if date >= 77+30
        logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using robust_binaryDV.doc, ctitle('main-one month') dec(2)
        restore


        preserve
        drop if (date < 77+30 & date >= 77)
        drop if date >= 77+60
        logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using robust_binaryDV.doc, ctitle('main-month 2nd') dec(2)
        restore


        preserve
        drop if (date < 77+60 & date >= 77)
        drop if date >= 77+90
        logit togetherb_avg_B post treated treatedPost i.hour, robust cluster(advertiser_id)
        outreg2 using robust_binaryDV.doc, ctitle('main-month 3rd') dec(2)
        restore


    ###

###













