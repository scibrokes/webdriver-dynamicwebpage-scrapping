# -*- coding: utf-8 -*-
"""
Created on Fri Nov 08 23:12:57 2013
@author: Scibrokes
"""
# ============================================================
#' import codecs
#' import requests
#' import html5lib
#' import string
import lxml.html as lh
from lxml import etree
import urllib, urllib2
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from pandas import *
import unittest, time, re
from datetime import datetime
from dateutil import parser
import inspect
import itertools
#' import HTMLParser

chromedriver = "chromedriver.exe" #32bit driver
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
#browser.implicitly_wait(60) #set driver waiting period to be 60seconds

def makelist(table):
  result = []
  allrows = table.findAll('tr')
  for row in allrows[5:16]: #from row 5 to 16
    result.append([])
    allcols = row.findAll('td')
    for col in allcols:
      thestrings = [unicode(s) for s in col.findAll(text=True)]
      thetext = ''.join(thestrings)
      result[-1].append(thetext)
  return result

def get_web_table(URL):
    browser.get(URL)
    # read page html source codes
    content = browser.page_source
    soup = BeautifulSoup(''.join(content))

    dflist = []
    num1 = soup.findAll('table')[2].findAll('tr')
    k = 0
    for i in range(1,len(num1)+1):
        for j in range(1,len(num1[i-1])+1):
            k = k + 1
            # click button on website
            clickme = browser.find_element_by_xpath('//*[@id="e_run_tb"]/tbody/tr'+'['+str(i)+']'+'/td'+'['+str(j)+']')
            clickme.click()
            content = browser.page_source
            soup = BeautifulSoup(''.join(content))
            table = soup.find('div', attrs={'class': 'e_matches'})
            tab_list = makelist(table)
            df = DataFrame(tab_list[1:len(tab_list)],columns=('Round','Date','Home','Score','Away','NULL'))
            dflist.append(df)
    pandas.set_option('display.height', 500)
    pandas.set_option('display.max_rows', 500)
    dfm = dflist[0]
    i = 1
    while i < len(dflist):
        dfm = dfm.append(dflist[i])
        i = i + 1
    dfm.Home = dfm.Home.str.replace("[^ 0-9a-zA-Z ]","")
    dfm.Away = dfm.Away.str.replace("[^ 0-9a-zA-Z ]","")
    df = DataFrame(dfm.Score.str.split('[-()]').tolist(),columns = ['FTHG','FTAG','HTHG','HTAG','NULL']).drop('NULL',1)
    tab = merge(dfm,df,on=df.index,how='outer').drop('Score',1)
    return tab.ix[:len(tab),:len(tab.columns)]

# http://data2.7m.cn/database/index_en.htm
# node xpath of English soccer league
# clickme = browser.find_element_by_xpath('//*[@id="content1111"]/ul/li[1]/table/tbody/tr[2]/td/span')
URL0910 = 'http://data2.7m.cn/history_Matches_Data/2009-2010/92/en/index.shtml'
URL1011 = 'http://data2.7m.cn/history_Matches_Data/2010-2011/92/en/index.shtml'
URL1112 = 'http://data2.7m.cn/history_Matches_Data/2011-2012/92/en/index.shtml'
#URL1213 = 'http://data2.7m.cn/history_Matches_Data/2012-2013/92/en/index.shtml'

# run the function to scrap the web content to be data frame
eng0910 = get_web_table(URL0910).drop('NULL',1)
eng1011 = get_web_table(URL1011).drop('NULL',1)
eng1112 = get_web_table(URL1112).drop('NULL',1)
#eng1213 = get_web_table(URL1213).drop('NULL',1)
del URL0910;del URL1011;del URL1112;#del URL1213

###############################################################
# filter unique date id
def get_dateID(dfm):
    date_data = array(DataFrame(dfm.Date.str.split(' ').tolist(),columns=['Date','Time']).drop('Time',1))
    seen = set() # set of seen values, which starts out empty
    for lst in date_data:
        deduped = [x for x in lst if x not in seen] # filter out previously seen values
        seen.update(deduped)                        # add the new values to the set
    date_list = [parser.parse(date).strftime('%Y-%m-%d') for date in seen]
    return date_list

dateID = get_dateID(eng1112)
#URL = 'http://odds.7m.hk/en/default.shtml?t=3&dt=2011-08-20'
URL = str('http://odds.7m.hk/en/default.shtml?t=3&dt=')
URL_list = []
for i in range(len(dateID)-1):
    date_data = URL + dateID[i]
    URL_list.append(date_data)
del date_data

#open odds price webpage
browser.get(URL_list[0])

#uncheck the default checked checkboxes in Bookmaker Selection checkboxes
checkboxes = browser.find_elements_by_xpath('//input[@name="c_provider" and @checked="checked"]')
for checkbox in checkboxes:
    if checkbox.is_selected():
        checkbox.click()

#reselect/check all 11 bookmakers in list
for i in range(1,12): #reselect the 11 bookmakers (11 are default all bookmakers in list)
    browser.find_element_by_xpath('//*[@id="cf_list"]/li['+str(i)+']/label/input').click()
browser.find_element_by_xpath('//*[@id="cf_input"]/span[1]/a').click()

#expend the wrapped/collapsed event list which includes leagues
browser.find_element_by_xpath('//*[@id="hlistMatch"]').click()

#only omit the checkbox ENG Premier League id @value='92'
checkboxes = browser.find_elements_by_xpath('//input[@name="c_league" and not(@value="92") and @checked="checked"]')
for checkbox in checkboxes:
    if checkbox.is_selected():
        checkbox.click()
browser.find_element_by_xpath('//*[@id="league_input"]/span[1]/a').click()

#get xml frame content
frame = browser.find_element_by_xpath('//*[@id="Matchframe"]')
browser.switch_to_frame(frame)
#get page source
content = browser.page_source
soup = BeautifulSoup(''.join(content))
#print soup.prettify()

# ===============================================================
def get_matchID(URL):
    # filter match id, next step will be scrap the odds price
    matchID = []
    # open odds price webpage
    for i in range(len(URL)):
        browser.get(URL[i])
        # uncheck the default checked checkboxes in Bookmaker Selection checkboxes
        checkboxes = browser.find_elements_by_xpath('//input[@name="c_provider" and @checked="checked"]')
        for checkbox in checkboxes:
            if checkbox.is_selected():
                checkbox.click()
        # reselect/check all 11 bookmakers in list
        for i in range(1,12): #reselect the 11 bookmakers (11 are default all bookmakers in list)
            browser.find_element_by_xpath('//*[@id="cf_list"]/li['+str(i)+']/label/input').click()
        browser.find_element_by_xpath('//*[@id="cf_input"]/span[1]/a').click()
        # expend the wrapped/collapsed event list which includes leagues
        browser.find_element_by_xpath('//*[@id="hlistMatch"]').click()
        # only omit the checkbox ENG Premier League id @value='92'
        checkboxes = browser.find_elements_by_xpath('//input[@name="c_league" and not(@value="92") and @checked="checked"]')
        for checkbox in checkboxes:
            if checkbox.is_selected():
                checkbox.click()
        browser.find_element_by_xpath('//*[@id="league_input"]/span[1]/a').click()
        # get xml frame content
        frame = browser.find_element_by_xpath('//*[@id="Matchframe"]')
        browser.switch_to_frame(frame)
        # get page source
        content = browser.page_source
        soup = BeautifulSoup(''.join(content))
        # scrap links which are include EngPR leagueID 92, and also matchID
        lnk = soup.findAll('a', attrs={'class':['team_ls','lot_icon0'],
                                       'href':re.compile('http://data.7m.cn/matches_data/92/en/index.shtml|http://data.7m.cn/analyse/en/')})
        EngPR = soup.findAll('a', href=re.compile('http://data.7m.cn/matches_data/92/en/index.shtml'))
        # filter and only get matchID inside EngPR
        df = lnk
        for i in range(len(lnk)):
            if EngPR[0]['href'] == lnk[i]['href']:
                # re.findall(r'.*?([0-9]+)', dflist[0])
                # Out[162]: ['7', '473558']
                # [-1] to delete the 1st matched digit which is http://data.'7'm.cn
                df = re.findall(r'.*?([0-9]+)', lnk[i+1]['href'])[-1]
                matchID.append(df)
        del lnk; del EngPR; del df; del i
    return matchID


# --------------------------------------------------------------
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 00:34:29 2014
@author: Scibrokes Trading
"""
# ============================================================
import lxml.html as lh
from lxml import etree
import urllib, urllib2
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from pandas import *
import unittest, time, re
from datetime import datetime
from dateutil import parser
import inspect
import itertools
import HTMLParser
import string
import win32com.client
import pyodbc, pypyodbc
import sqlite3
import pandas.io.sql as sql
pandas.set_option('display.max_rows', 50000)
pandas.set_option('display.height', 50000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 500)

# ===============================================================
def makeList(table):
  # internal function located in get_web_table(URL)
    result = []; i=0; j=0
    allrows = table.findAll('tr')
    for i in range(len(allrows)):
        result.append([])
        allcols = allrows[i].findAll('td')
        for j in range(len(allcols)):
            thestrings = allcols[j].findAll(text=True)
            if i>0 and j == (len(allcols)-1):
                thestrings = re.findall(r'.*?([0-9]+)',str(allcols[j]))[0] #get 1st element which is matchID
            thetext = ''.join(thestrings)
            result[-1].append(thetext)
    return result

# ===============================================================
def get_web_table(URL):
    # url1112 = 'http://data2.7m.cn/history_Matches_Data/2011-2012/92/en/index.shtml'
    # eng1112 = get_web_table(url1112)
    browser.get(URL)
    # time.sleep(5)
    # read page html source codes
    content = browser.page_source
    soup = BeautifulSoup(''.join(content))
    dflist = []
    num1 = soup.findAll('table')[2].findAll('tr')
    k = 0
    for i in range(1,len(num1)+1):
        for j in range(1,len(num1[i-1])+1):
            k = k + 1
            # click button on website
            clickme = browser.find_element_by_xpath('//*[@id="e_run_tb"]/tbody/tr'+'['+str(i)+']'+'/td'+'['+str(j)+']')
            clickme.click()
            content = browser.page_source
            soup = BeautifulSoup(''.join(content))
            table = soup.find('div', attrs={'id': 'Match_Table'})
            tab_list = makeList(table) # call makelist function
            df = DataFrame(tab_list[1:len(tab_list)],columns=('Round','KODate','Home','Score','Away','MatchID'))
            dflist.append(df)
    dfm = dflist[0]
    i = 1
    while i < len(dflist):
        dfm = dfm.append(dflist[i])
        i = i + 1
    dfm.Home = dfm.Home.str.replace("[^ 0-9a-zA-Z ]", "")
    dfm.Away = dfm.Away.str.replace("[^ 0-9a-zA-Z ]", "")
    df = DataFrame(dfm.Score.str.split('[-()]').tolist(),columns = ['FTHG','FTAG','HTHG','HTAG','NULL']).drop('NULL',1)
    tab = merge(dfm, df, on = df.index, how = 'outer').drop('Score', 1)
    # correct the kick-off date as some less a year
#   tab.KODate = tab.KODate.astype('datetime64[ns]')
    for i in range(len(tab.KODate)):
        if tab.KODate[i] < tab.KODate[0]:
            if str(tab.KODate[i]).split('-')[0] == str(tab.KODate[0]).split('-')[0]:
                newdate = int(str(tab.KODate[i]).split('-')[0]) + 1
                tab.KODate[i] = re.sub(str(tab.KODate[i]).split('-')[0], str(newdate), str(tab.KODate[i]))
#   tab.KODate = tab.KODate.astype('datetime64[ns]')
    tab.Round.convert_objects(convert_numeric=True)
    tab.MatchID.convert_objects(convert_numeric=True)
    tab.FTHG.convert_objects(convert_numeric=True)
    tab.FTAG.convert_objects(convert_numeric=True)
    tab.HTHG.convert_objects(convert_numeric=True)
    tab.HTAG.convert_objects(convert_numeric=True)
    return tab

# ===============================================================
def get_AHOU(matchID):
    # url_WDW = 'http://odds.7m.hk/en/1x2.shtml?id='
    url_AH = 'http://odds.7m.hk/en/odds.shtml?id='
    url_OU = 'http://odds.7m.hk/en/overunder.shtml?id='
    # re.sub('=.*([\w.-]+)','',URL)+'='
    # WDW1112_matchID = url_WDW + eng1112.Analysis
    matchID_AH = url_AH + str(matchID)
    matchID_OU = url_OU + str(matchID)
    AH = get_odds_history(matchID_AH, odds_Type='AH')
    OU = get_odds_history(matchID_OU, odds_Type='OU')
    return AH,OU

# ===============================================================
def get_odds_history(matchID, odds_Type):
    # eng1112 = get_web_table(url1112)
    # 
    if odds_Type == 'AH':
        odds = ('_AH', '_HM', '_AW')
        odds_attrs = {'id': 'odds_his'}
    if odds_Type == 'OU':
        odds = ('_OU', '_OV', '_UN')
        odds_attrs = {'id': 'over_his'}
    browser.get(matchID)
    # time.sleep(5)
    content = browser.page_source
    soup = BeautifulSoup(''.join(content))
    table = soup.findAll('div', attrs = odds_attrs)
    result = []
    for tab in table:
        allrows = tab.findAll('tr')
        for row in allrows:
            result.append([])
            allcols = row.findAll(re.compile('td|span'))
            for col in allcols:
                tab = col.findAll(text=True)
                if len(tab) == 0:
                    result[-1].extend(['',''])
                if len(tab) > 1:
                    # only get 1st element inside a box
                    tab = col.findAll(text=True)[0]
                thetext = ''.join(tab)
                result[-1].append(thetext)
        colname = tuple(allrows[0].findAll(text=True))
    resname = ()
    for i in range(len(colname[:-1])):
        newname = colname[i]+odds[0], colname[i]+odds[1], colname[i]+odds[2]
        resname = resname + newname
    resname = resname, colname[-1]
    resname = resname[0] + (resname[1],)
    df = DataFrame(result[1:-1], columns=resname)
    #filter only AH/OU handicap column
    colname = df.filter(regex=odds[0]).columns
    for i in range(len(colname)):
        df1 = df[colname[i]].str.replace('/.*([\w.-]+)','')
        df1 = df1.str.replace('^-','').convert_objects(convert_numeric=True)
        df2 = df[colname[i]].str.replace('([\w.-]+).*/','')
        df2 = df2.str.replace('^-','').convert_objects(convert_numeric=True)
        symb = df[colname[i]].str.replace('[^-]','')
        cdf = (df1 + df2)/2
        hdp = []
        for j in range(len(cdf)):
            hand = symb[j] + str(cdf[j])
            if hand == 'nan':
                hand = ''
            hdp.append(hand)
        df[colname[i]] = hdp
    #fill odds price in the blanks
    for i in range(len(df.columns)-1):
        for j in reversed(df.index[:-1]):
            if df[df.columns[i]][j] == '':
                df[df.columns[i]][j] = df[df.columns[i]][j+1]
            if df[df.columns[i]][j] is not '':
                df[df.columns[i]][j] = df[df.columns[i]][j]
    return df

# ========================================================
def create_mdb(path, filename):
    # create folder and *.mdb database file.
    # ex1: create_mdb('E:/Database/England/Eng PR/','test')
    # ex2: create_mdb('E:/Database/England/Eng PR','test')
    # ex3: create_mdb('E:/Database/England/Eng PR/','test.mdb')
    # ex4: create_mdb('E:/Database/England/Eng PR','test.mdb')
    path = str(path)
    filename = re.sub('.mdb$','',filename)
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.isfile(path + '/' + filename + '.mdb'):
        return None
    if not os.path.isfile(path + '/' + filename + '.mdb'):
        oAccess = win32com.client.Dispatch('Access.Application')
        DbFile = path + '/' + filename + '.mdb'
        dbLangGeneral = ';LANGID=0x0409;CP=1252;COUNTRY=0'
        # dbVersion40 64
        dbVersion = 64
        oAccess.DBEngine.CreateDatabase(DbFile, dbLangGeneral, dbVersion)
        oAccess.Quit()
        del oAccess
    return None

# ========================================================
def create_mdb(path, filename):
    if not os.path.exists(path):
        os.makedirs(path)
    return pypyodbc.win_create_mdb(path + filename)

# ========================================================
def create_mdb_table(Country, League, filename):
    # create folder and *.mdb database file.
    newpath = 'E:/Database/' + Country + '/' + League
    filename = re.sub('.mdb$','',filename)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    if os.path.isfile(newpath + '/' + filename + '.mdb'):
        return None
    if not os.path.isfile(newpath + '/' + filename + '.mdb'):
        oAccess = win32com.client.Dispatch('Access.Application')
        DbFile = newpath + '/' + filename + '.mdb'
        dbLangGeneral = ';LANGID=0x0409;CP=1252;COUNTRY=0'
        # dbVersion40 64
        dbVersion = 64
        oAccess.DBEngine.CreateDatabase(DbFile, dbLangGeneral, dbVersion)
        oAccess.Quit()
        del oAccess
    constrings = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' \
                 'DBQ=E:\\Database\\' + Country + '\\' + League + '\\' \
                 + filename + '.mdb'
    con = pyodbc.connect(constrings)
    cur = con.cursor()
    table = '''CREATE TABLE Matches (key_0 COUNTER PRIMARY KEY, Round int, 
                                     KODate datetime, Home varchar(30), 
                                     Away varchar(30), MatchID int, FTHG int, 
                                     FTAG int, HTHG int, HTAG int);'''
    cur.execute(table)
    con.commit()
    con.close()
    return None

# ===============================================================
def get_dateID(dfm, link=False):
    dateID = []    
    for i in range(len(dfm.KODate)):
        dt = dfm.KODate[i].strftime('%Y-%m-%d')        
        dateID.append(dt)
    date_list = sorted(tuple(set(dateID)))
    # if link==True, then we can apply it for get_matchID use
    if link == True:
        #URL = 'http://odds.7m.hk/en/default.shtml?t=3&dt=2011-08-20'
        URL = str('http://odds.7m.hk/en/default.shtml?t=3&dt=')
        URL_list = []
        for i in range(len(date_list)-1):
            date_data = URL + date_list[i]
            URL_list.append(date_data)
        del date_data
        date_list = tuple(URL_list)
    return tuple(date_list)

# ============================================================
