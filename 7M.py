# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 13:30:44 2014

@author: Scibrokes Trading
"""
# ================================================================
# need to load and run the Pymodel.py script

# get soccer matches and odds from NowGoal website
# open chromedriver
chromedriver = "chromedriver_win32.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
browser.set_window_size(1015, 600)
browser.set_window_position(0, 200)
#time.sleep(2) #waiting period 2 seconds
#browser.implicitly_wait(60) #set driver waiting period to be 60seconds

# http://data2.7m.cn/database/index_en.htm
url0910 = 'http://data2.7m.cn/history_Matches_Data/2009-2010/92/en/index.shtml'
url1011 = 'http://data2.7m.cn/history_Matches_Data/2010-2011/92/en/index.shtml'
url1112 = 'http://data2.7m.cn/history_Matches_Data/2011-2012/92/en/index.shtml'
url1213 = 'http://data2.7m.cn/history_Matches_Data/2012-2013/92/en/index.shtml'
url1314 = 'http://data2.7m.cn/matches_data/92/en/index.shtml'

# run the function to scrap the web content to be data frame
eng0910 = get_7M_matches(url0910,tz='GMT+0')
eng1011 = get_7M_matches(url1011,tz='GMT+0')
eng1112 = get_7M_matches(url1112,tz='GMT+0')
eng1213 = get_7M_matches(url1213,tz='GMT+0')
eng1314 = get_7M_matches(url1314,tz='GMT+0')

del url0910
del url1011
del url1112
del url1213
del url1314

# -----------------------------------------------------------
# save soccer matches into xlsx file
path = 'E:/Database/England/Eng_PR/'
saveMDB(path, dbase=eng0910, filename='200910_7M')
saveMDB(path, dbase=eng1011, filename='201011_7M')
saveMDB(path, dbase=eng1112, filename='201112_7M')
saveMDB(path, dbase=eng1213, filename='201213_7M')
saveMDB(path, dbase=eng1314, filename='201314_7M')

# -----------------------------------------------------------
# save AH and OU odds with matchID into xlsx file
path = 'E:/Database/England/Eng_PR/'
url_AH = 'http://odds.7m.hk/en/odds.shtml?id='
url_OU = 'http://odds.7m.hk/en/overunder.shtml?id='
for i in range(len(eng1213.MatchID)):
    match = get_7M_AHOU(eng1213.MatchID[i],tz='GMT+0')
    if url_AH in match[0]:
        print i,match[0]
    if url_OU in match[1]:
        print i,match[1]
    saveMDB(path, dbase=match, filename=eng1213.MatchID[i], dataType='odds')

# missing below webpage content:
eng1213.MatchID[20] # 782090 missed both AH & OU ### nowgoal 710945
eng1213.MatchID[53] # 782290 missed both AH & OU ### nowgoal 710971
eng1213.MatchID[89] # 782451 missed both AH & OU ### nowgoal 710998
eng1213.MatchID[151] # http://odds.7m.hk/en/overunder.shtml?id=783056 ### nowgoal 711067
eng1213.MatchID[152] # http://odds.7m.hk/en/overunder.shtml?id=783063 ### nowgoal 711071
eng1213.MatchID[153] # http://odds.7m.hk/en/overunder.shtml?id=783065 ### nowgoal 711072
eng1213.MatchID[154] # http://odds.7m.hk/en/overunder.shtml?id=783067 ### nowgoal 711073
eng1213.MatchID[155] # http://odds.7m.hk/en/overunder.shtml?id=783071 ### nowgoal 711075
eng1213.MatchID[156] # http://odds.7m.hk/en/overunder.shtml?id=783061 ### nowgoal 711070
eng1213.MatchID[157] # http://odds.7m.hk/en/overunder.shtml?id=783057 ### nowgoal 711068
eng1213.MatchID[158] # http://odds.7m.hk/en/overunder.shtml?id=783069 ### nowgoal 711074
eng1213.MatchID[159] # http://odds.7m.hk/en/overunder.shtml?id=783059 ### nowgoal 711069
eng1213.MatchID[188] # http://odds.7m.hk/en/odds.shtml?id=783189 ### nowgoal 711104

path = 'E:/Database/England/Eng_PR/'
urlAHOU = 'http://data.nowgoal.com/oddscomp/'
NowGoal_matchID=['710945','710971','710998','711067','711071','711072','711073','711075','711070','711068','711074','711069','711104']
for i in range(len(NowGoal_matchID)):
    match = get_NowGoal_AHOU(NowGoal_matchID[i])
    if urlAHOU in match[0]:
        print i,match[0]
    if urlAHOU in match[1]:
        print i,match[1]
    saveMDB(path, dbase=match, filename=NowGoal_matchID[i], URL='NowGoal',dataType='odds')

# -----------------------------------------------------------
dateID = get_dateID(eng1112)

# ================================================================



