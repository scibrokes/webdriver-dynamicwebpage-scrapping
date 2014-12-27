# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 13:30:47 2014

@author: Scibrokes Trading
"""
# ===========================================================
# get soccer matches and odds from NowGoal website
# open chromedriver
chromedriver = "chromedriver_win32.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
browser.set_window_size(1015, 600)
browser.set_window_position(0, 200)

url0910 = 'http://info.nowgoal.com/en/League.aspx?matchSeason=2009-2010&sclassID=36&lang=2'
url1011 = 'http://info.nowgoal.com/en/League.aspx?matchSeason=2010-2011&sclassID=36&lang=2'
url1112 = 'http://info.nowgoal.com/en/League.aspx?matchSeason=2011-2012&sclassID=36&lang=2'
url1213 = 'http://info.nowgoal.com/en/League.aspx?matchSeason=2012-2013&sclassID=36&lang=2'
url1314 = 'http://info.nowgoal.com/en/League.aspx?matchSeason=2013-2014&sclassID=36&lang=2'

# run the function to scrap the web content to be data frame
eng0910 = get_NowGoal_matches(url0910)
eng1011 = get_NowGoal_matches(url1011)
eng1112 = get_NowGoal_matches(url1112)
eng1213 = get_NowGoal_matches(url1213)
eng1314 = get_NowGoal_matches(url1314)

del url0910
del url1011
del url1112
del url1213
del url1314

# -----------------------------------------------------------
# save soccer matches into xlsx file
path = 'E:/Database/England/Eng_PR/'
saveMDB(path, dbase=eng0910, filename='200910_NG', URL='NowGoal')
saveMDB(path, dbase=eng1011, filename='201011_NG', URL='NowGoal')
saveMDB(path, dbase=eng1112, filename='201112_NG', URL='NowGoal')
saveMDB(path, dbase=eng1213, filename='201213_NG', URL='NowGoal')
saveMDB(path, dbase=eng1314, filename='201314_NG', URL='NowGoal')

# -----------------------------------------------------------
# save AH and OU odds with matchID into xlsx file
path = 'E:/Database/England/Eng_PR/'
urlAHOU = 'http://data.nowgoal.com/oddscomp/'
for i in range(len(eng1213.MatchID)):
    match = get_NowGoal_AHOU(eng1213.MatchID[i])
    if urlAHOU in match[0]:
        print i,match[0]
    if urlAHOU in match[1]:
        print i,match[1]
    saveMDB(path, dbase=match, filename=eng1213.MatchID[i], URL='NowGoal',dataType='odds')

# -----------------------------------------------------------



