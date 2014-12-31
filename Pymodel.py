# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 00:34:29 2014
@author: Scibrokes Trading
"""
# ============================================================
import lxml.html as lh
from lxml import etree
import urllib, urllib3
import os, os.path
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
from datetime import datetime, timedelta
from dateutil import parser
import inspect
import itertools
from html.parser import HTMLParser
import string
import win32com.client
import pypyodbc#, pyodbc
import sqlite3#, oursql
import pandas.io.sql as pd_sql
#'import mysql.connector as sql_conn
#'import PyMySQL

# get soccer matches and odds from NowGoal website
# open chromedriver
#'chromedriver = "chromedriver.exe" # win32
#'os.environ["webdriver.chrome.driver"] = chromedriver
#'browser = webdriver.Chrome(chromedriver)
browser = webdriver.Chrome()
browser.set_window_size(1015, 600)
browser.set_window_position(0, 200)
#time.sleep(2) #waiting period 2 seconds
#browser.implicitly_wait(60) #set driver waiting period to be 60seconds

pandas.set_option('display.max_rows', 50000)
pandas.set_option('display.height', 50000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 500)

# ===============================================================
def GMT(tz, daylightsaving, method):
    if method == 'web':
        timezone = 'http://data2.7m.cn/timezone/timezone_en.htm'
        browser.get(timezone)
    if method == 'click':
        browser.find_element_by_xpath('//*[@id="TimeZone"]').click()
    if tz == 'Auto':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[1]').click()
    if tz == 'GMT-1200'or tz == 'GMT-12':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[2]').click()
    if tz == 'GMT-1100'or tz == 'GMT-11':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[3]').click()
    if tz == 'GMT-1000'or tz == 'GMT-10':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[4]').click()
    if tz == 'GMT-0900'or tz == 'GMT-09'or tz == 'GMT-9':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[5]').click()
    if tz == 'GMT-0800'or tz == 'GMT-08'or tz == 'GMT-8':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[6]').click()
    if tz == 'GMT-0700'or tz == 'GMT-07'or tz == 'GMT-7':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[7]').click()
    if tz == 'GMT-0600'or tz == 'GMT-06'or tz == 'GMT-6':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[10]').click()
    if tz == 'GMT-0500'or tz == 'GMT-05'or tz == 'GMT-5':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[13]').click()
    if tz == 'GMT-0400'or tz == 'GMT-04'or tz == 'GMT-4':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[17]').click()
    if tz == 'GMT-0300'or tz == 'GMT-03'or tz == 'GMT-3':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[24]').click()
    if tz == 'GMT-0200'or tz == 'GMT-02'or tz == 'GMT-2':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[25]').click()
    if tz == 'GMT-0100'or tz == 'GMT-01'or tz == 'GMT-1':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[26]').click()
    if tz == 'GMT+0000'or tz == 'GMT+00'or tz == 'GMT+0':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[30]').click()
    if tz == 'GMT+0100'or tz == 'GMT+01'or tz == 'GMT+1':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[33]').click()
    if tz == 'GMT+0200'or tz == 'GMT+02'or tz == 'GMT+2':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[38]').click()
    if tz == 'GMT+0300'or tz == 'GMT+03'or tz == 'GMT+3':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[43]').click()
    if tz == 'GMT+0400'or tz == 'GMT+04'or tz == 'GMT+4':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[49]').click()
    if tz == 'GMT+0500'or tz == 'GMT+05'or tz == 'GMT+5':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[51]').click()
    if tz == 'GMT+0600'or tz == 'GMT+06'or tz == 'GMT+6':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[56]').click()
    if tz == 'GMT+0700'or tz == 'GMT+07'or tz == 'GMT+7':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[57]').click()
    if tz == 'GMT+0800'or tz == 'GMT+08'or tz == 'GMT+8':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[59]').click()
    if tz == 'GMT+0900'or tz == 'GMT+09'or tz == 'GMT+9':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[60]').click()
    if tz == 'GMT+1000'or tz == 'GMT+10':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[64]').click()
    if tz == 'GMT+1100'or tz == 'GMT+11':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[65]').click()
    if tz == 'GMT+1200'or tz == 'GMT+12':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[67]').click()
    #daylight saving
    if daylightsaving == 'Y'or daylightsaving == 'Yes'or daylightsaving == 'T'\
       or daylightsaving == 'True':
        browser.find_element_by_xpath('//*[@id="DSTbox"]').click()
    return browser.find_element_by_xpath('//*[@id="CloImg"]').click()

# ===============================================================
def areaGMT(tz, daylightsaving, method):
    if method == 'web':
        timezone = 'http://data2.7m.cn/timezone/timezone_en.htm'
        browser.get(timezone)
    if method == 'click':
        browser.find_element_by_xpath('//*[@id="TimeZone"]').click()
        tzwin = browser.find_element_by_xpath('//*[@id="Time_Zone_List"]/iframe')
        browser.switch_to_frame(tzwin)
    if tz == 'Auto':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[1]').click()
    if tz == 'GMT-1200'or tz == 'GMT-12':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[2]').click()
    if tz == 'GMT-1100'or tz == 'GMT-11':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[3]').click()
    if tz == 'GMT-1000'or tz == 'GMT-10':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[4]').click()
    if tz == 'GMT-0900'or tz == 'GMT-09'or tz == 'GMT-9':
        browser.find_element_by_xpath('//*[@id="Map"]/area[44]').click()
    if tz == 'GMT-0800'or tz == 'GMT-08'or tz == 'GMT-8':
        browser.find_element_by_xpath('//*[@id="Map"]/area[43]').click()
    if tz == 'GMT-0700'or tz == 'GMT-07'or tz == 'GMT-7':
        browser.find_element_by_xpath('//*[@id="Map"]/area[35]').click()
    if tz == 'GMT-0600'or tz == 'GMT-06'or tz == 'GMT-6':
        browser.find_element_by_xpath('//*[@id="Map"]/area[35]').click()
    if tz == 'GMT-0500'or tz == 'GMT-05'or tz == 'GMT-5':
        browser.find_element_by_xpath('//*[@id="Map"]/area[29]').click()
    if tz == 'GMT-0400'or tz == 'GMT-04'or tz == 'GMT-4':
        browser.find_element_by_xpath('//*[@id="Map"]/area[41]').click()
    if tz == 'GMT-0300'or tz == 'GMT-03'or tz == 'GMT-3':
        browser.find_element_by_xpath('//*[@id="Map"]/area[47]').click()
    if tz == 'GMT-0200'or tz == 'GMT-02'or tz == 'GMT-2':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[25]').click()
    if tz == 'GMT-0100'or tz == 'GMT-01'or tz == 'GMT-1':
        browser.find_element_by_xpath('//*[@id="TimeZone"]/option[26]').click()
    if tz == 'GMT+0000'or tz == 'GMT+00'or tz == 'GMT+0':
        browser.find_element_by_xpath('//*[@id="Map"]/area[26]').click()
    if tz == 'GMT+0100'or tz == 'GMT+01'or tz == 'GMT+1':
        browser.find_element_by_xpath('//*[@id="Map"]/area[24]').click()
    if tz == 'GMT+0200'or tz == 'GMT+02'or tz == 'GMT+2':
        browser.find_element_by_xpath('//*[@id="Map"]/area[18]').click()
    if tz == 'GMT+0300'or tz == 'GMT+03'or tz == 'GMT+3':
        browser.find_element_by_xpath('//*[@id="Map"]/area[17]').click()
    if tz == 'GMT+0400'or tz == 'GMT+04'or tz == 'GMT+4':
        browser.find_element_by_xpath('//*[@id="Map"]/area[15]').click()
    if tz == 'GMT+0500'or tz == 'GMT+05'or tz == 'GMT+5':
        browser.find_element_by_xpath('//*[@id="Map"]/area[13]').click()
    if tz == 'GMT+0600'or tz == 'GMT+06'or tz == 'GMT+6':
        browser.find_element_by_xpath('//*[@id="Map"]/area[11]').click()
    if tz == 'GMT+0700'or tz == 'GMT+07'or tz == 'GMT+7':
        browser.find_element_by_xpath('//*[@id="Map"]/area[10]').click()
    if tz == 'GMT+0800'or tz == 'GMT+08'or tz == 'GMT+8':
        browser.find_element_by_xpath('//*[@id="Map"]/area[1]').click()
    if tz == 'GMT+0900'or tz == 'GMT+09'or tz == 'GMT+9':
        browser.find_element_by_xpath('//*[@id="Map"]/area[6]').click()
    if tz == 'GMT+1000'or tz == 'GMT+10':
        browser.find_element_by_xpath('//*[@id="Map"]/area[7]').click()
    if tz == 'GMT+1100'or tz == 'GMT+11':
        browser.find_element_by_xpath('//*[@id="Map"]/area[4]').click()
    if tz == 'GMT+1200'or tz == 'GMT+12':
        browser.find_element_by_xpath('//*[@id="Map"]/area[45]').click()
    #daylight saving
    if daylightsaving == 'Y'or daylightsaving == 'Yes'or daylightsaving == 'T'\
       or daylightsaving == 'True':
        browser.find_element_by_xpath('//*[@id="DSTbox"]').click()
    return browser.find_element_by_xpath('//*[@id="CloImg"]').click()

# ===============================================================
def make_7M_list(table):
  # internal function located in get_7M_matches(URL)
    result = []; i=0; j=0
    allrows = table.findAll('tr')
    for i in range(len(allrows)):
        result.append([])
        allcols = allrows[i].findAll('td')
        for j in range(len(allcols)):
            thestrings = allcols[j].findAll(text=True)
            if i>0 and j == (len(allcols)-1):
                #get 1st element which is matchID
                thestrings = re.findall(r'.*?([0-9]+)',str(allcols[j]))[0]
            thetext = ''.join(thestrings)
            result[-1].append(thetext)
    return result

# ===============================================================
def get_7M_matches(URL, tz='Auto', daylightsaving='No'):
    # URL='http://data2.7m.cn/history_Matches_Data/2011-2012/92/en/index.shtml'
    # tz='GMT+0' #tz='GMT+00'or tz='GMT+0000' either 1,2 or 4 digits also work.
    # eng1112 = get_7M_matches(URL,tz)
    #GMT(tz,daylightsaving,'web')
    areaGMT(tz=tz, daylightsaving=daylightsaving, method='web')
    browser.get(URL)
    #time.sleep(5)
    #browser.refresh()
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
            tab_list = make_7M_list(table) # call makelist function
            df = DataFrame(tab_list[1:len(tab_list)],columns=('Round','KODate','Home','Score','Away','MatchID'))
            dflist.append(df)
    dfm = dflist[0]
    i = 1
    while i < len(dflist):
        dfm = dfm.append(dflist[i])
        i = i + 1
    dfm = dfm.dropna(how='any')
    dfm.Home = dfm.Home.str.replace("[^ 0-9a-zA-Z ]", "")
    dfm.Away = dfm.Away.str.replace("[^ 0-9a-zA-Z ]", "")
    df = DataFrame(dfm.Score.str.split('[-()]').tolist(),columns = ['FTHG','FTAG','HTHG','HTAG','NULL']).drop('NULL',1)
    tab = merge(dfm, df, on = df.index, how = 'outer').drop('Score', 1)
    # -----------------------------------------------------------
    def to_number(s, varType):
        try:
            s1 = varType(s)
            return s1
        except ValueError:
            return s
    # -----------------------------------------------------------
    tab = tab[['MatchID','Round','KODate','Home','Away','FTHG','FTAG','HTHG','HTAG']]
    tab.MatchID = tab.apply(lambda f : to_number(f[0], int) , axis = 1)
    tab.Round   = tab.apply(lambda f : to_number(f[1], int) , axis = 1)
    tab.KODate  = to_datetime(tab.KODate, dayfirst=True)
    tab.Home    = tab.apply(lambda f : to_number(f[3], str) , axis = 1)
    tab.Away    = tab.apply(lambda f : to_number(f[4], str) , axis = 1)
    tab.FTHG    = tab.apply(lambda f : to_number(f[5], int) , axis = 1)
    tab.FTAG    = tab.apply(lambda f : to_number(f[6], int) , axis = 1)
    tab.HTHG    = tab.apply(lambda f : to_number(f[7], int) , axis = 1)
    tab.HTAG    = tab.apply(lambda f : to_number(f[8], int) , axis = 1)
    return tab

# ===============================================================
def get_7M_AHOU(matchID, tz='Auto', daylightsaving='No'):
    # url_WDW = 'http://odds.7m.hk/en/1x2.shtml?id='
    url_AH = 'http://odds.7m.hk/en/odds.shtml?id='
    url_OU = 'http://odds.7m.hk/en/overunder.shtml?id='
    # re.sub('=.*([\w.-]+)','',URL)+'='
    # WDW1112_matchID = url_WDW + eng1112.Analysis
    matchID_AH = url_AH + str(matchID) # matchID.astype(str) #if df.matchID
    matchID_OU = url_OU + str(matchID) # matchID.astype(str) #if df.matchID
    AH = get_7M_odds(matchID_AH, odds_Type='AH', tz=tz, daylightsaving=daylightsaving)
    OU = get_7M_odds(matchID_OU, odds_Type='OU', tz=tz, daylightsaving=daylightsaving)
    return AH,OU

# ===============================================================
def get_7M_odds(matchID, odds_Type, tz, daylightsaving):
    if odds_Type == 'AH':
        odds = ('_AH', '_HM', '_AW')
        odds_attrs = {'id': 'odds_his'}
    if odds_Type == 'OU':
        odds = ('_OU', '_OV', '_UN')
        odds_attrs = {'id': 'over_his'}
    browser.get(matchID)
    areaGMT(tz=tz,daylightsaving=daylightsaving,method='click')
    time.sleep(5)
    #browser.refresh()
    content = browser.page_source
    soup = BeautifulSoup(''.join(content))
    table = soup.findAll('div', attrs = odds_attrs)
    if table[0].findAll('tr')==[]:
        return matchID
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
    df = merge(df[[-1]], df[df.columns[:-1]], on = df.index, how = 'outer')
    #filter only AH/OU handicap column
    colname = df.filter(regex=odds[0]).columns
    for i in range(len(colname)):
        df1 = df[colname[i]].str.replace('/.*([\w.-]+)','')
        df1 = df1.str.replace('^-','').convert_objects(convert_numeric=True)
        df2 = df[colname[i]].str.replace('([\w.-]+).*/','')
        df2 = df2.str.replace('^-','').convert_objects(convert_numeric=True)
        symb = df[colname[i]].str.replace('[^-]','')
        sdf = (df1 + df2)/2
        hdp = []
        for j in range(len(sdf)):
            hand = symb[j] + str(sdf[j])
            if hand == 'nan':
                hand = ''
            hdp.append(hand)
        df[colname[i]] = hdp
    #fill odds price in the blanks
    for i in range(1,len(df.columns)):
        for j in reversed(df.index[:-1]):
            if df[df.columns[i]][j] == '':
                df[df.columns[i]][j] = df[df.columns[i]][j+1]
            if df[df.columns[i]][j] is not '':
                df[df.columns[i]][j] = df[df.columns[i]][j]
    df = df.rename(columns = {'Time Updated':'Time_Updated'})
    df.Time_Updated = to_datetime(df.Time_Updated, dayfirst=True)
    return df[df.columns[1:]]

# ===============================================================
def make_NowGoal_list(table):
  # internal function located in get_NowGoal_matches(URL)
    result = []; i=0; j=0
    allrows = table.findAll('tr')
    for i in range(len(allrows)):
        result.append([])
        allcols = allrows[i].findAll('td')
        for j in range(len(allcols)):
            thestrings = allcols[j].findAll(text=True)
            if  (len(thestrings)>1)and(re.match(r'[0-9]',thestrings[0])is not None)\
            and(re.match(r'[0-9]',thestrings[1])is not None)and(thestrings[1][2]==':'):
                thetext = ' '.join(thestrings)
            elif(len(thestrings)>1)and(re.match(r'[0-9]',thestrings[0])is not None)\
            and(re.match(r'[0-9]',thestrings[1])is not None)and(thestrings[1][2]!=':'):
                result[-1].extend([thestrings[0],thestrings[1]])
            elif(len(thestrings)>1)and(re.match(r'[0-9]',thestrings[0])is not None)\
            and(re.match(r'[a-zA-Z]',thestrings[1])is not None):
                thetext = thestrings[1]
            elif(len(thestrings)>1)and(re.match(r'[a-zA-Z]',thestrings[0][0])is not None)\
            and(j is not (len(allcols)-1)):
                thetext = thestrings[0]
            elif i>0 and j == (len(allcols)-1):
                thestrings = re.findall(r'.*?([0-9]+)',str(allcols[j]))[0] #get 1st element which is matchID
                thetext = ''.join(thestrings)
            else:
                thetext = thestrings[0]
            result[-1].append(thetext)
    return result[2:len(result)-1]

# ===============================================================
def get_NowGoal_matches(URL):
    # url1112 = 'http://info.nowgoal.com/en/League.aspx?matchSeason=2012-2013&sclassID=36&lang=2'
    # eng1112 = get_NowGoal_matches(url1112)
    browser.get(URL)
    time.sleep(5)
    # read page html source codes
    content = browser.page_source
    soup = BeautifulSoup(''.join(content))
    dflist = []
    num1 = soup.find('table', attrs={'id': 'Table1'}).findAll(text=True)
    num1 =  re.sub(r'[^0-9]',',',str(num1)).split(',')
    num1 = [x for x in num1 if x != ''][1:]
    k = 0
    for i in range(1,3):
        for j in range(1,(len(num1)+2)/2):
            k = k + 1
            if i==1:
                j=j+1
            # click button on website
            clickme = browser.find_element_by_xpath('//*[@id="Table2"]/tbody/tr['+str(i)+']/td['+str(j)+']')
            clickme.click()
            content = browser.page_source
            soup = BeautifulSoup(''.join(content))
            table = soup.find('div', attrs={'class': 'tdsolid'})
            tab_list = make_NowGoal_list(table) # call makelist function
            df = DataFrame(tab_list,columns=('Round','KODate','NULL','FT','HT',\
            'Home','Away','NULL','NULL','NULL','NULL','MatchID')).drop('NULL',1)
            dflist.append(df)
    dfm = dflist[0]
    i = 1
    while i < len(dflist):
        dfm = dfm.append(dflist[i])
        i = i + 1
    dfm.index = range(len(dfm))
    dfm.Home = dfm.Home.str.replace('\(.*$', '')
    dfm.Away = dfm.Away.str.replace('\(.*$', '')
    FT = DataFrame(dfm.FT.str.split('-').tolist(),columns = ['FTHG','FTAG'])
    HT = DataFrame(dfm.HT.str.split('-').tolist(),columns = ['HTHG','HTAG'])
    df = merge(FT, HT, on = FT.index, how = 'outer')
    tab = merge(dfm, df[df.columns[1:]], on = dfm.index, how = 'outer').drop(['FT','HT'], 1)
    # correct the kick-off date as some less a year
#   tab.KODate = tab.KODate.astype('datetime64[ns]')
    yr1 = re.sub('[^0-9]','',URL)[0:4]
    tab.KODate = yr1+'-'+tab.KODate
    for i in range(len(tab.KODate)):
        if tab.KODate[i] < tab.KODate[0]:
            if str(tab.KODate[i]).split('-')[0] == str(tab.KODate[0]).split('-')[0]:
                newdate = int(str(tab.KODate[i]).split('-')[0]) + 1
                tab.KODate[i] = re.sub(str(tab.KODate[i]).split('-')[0], str(newdate), str(tab.KODate[i]))
    # -----------------------------------------------------------
    def to_number(s, varType):
        try:
            s1 = varType(s)
            return s1
        except ValueError:
            return s
    # -----------------------------------------------------------
    tab = tab[['MatchID','Round','KODate','Home','Away','FTHG','FTAG','HTHG','HTAG']]
    tab.MatchID = tab.apply(lambda f : to_number(f[0], int) , axis = 1)
    tab.Round   = tab.apply(lambda f : to_number(f[1], int) , axis = 1)
    tab.KODate  = to_datetime(tab.KODate, dayfirst=True)
    tab.Home    = tab.apply(lambda f : to_number(f[3], str) , axis = 1)
    tab.Away    = tab.apply(lambda f : to_number(f[4], str) , axis = 1)
    tab.FTHG    = tab.apply(lambda f : to_number(f[5], int) , axis = 1)
    tab.FTAG    = tab.apply(lambda f : to_number(f[6], int) , axis = 1)
    tab.HTHG    = tab.apply(lambda f : to_number(f[7], int) , axis = 1)
    tab.HTAG    = tab.apply(lambda f : to_number(f[8], int) , axis = 1)
    return tab

# ================================================================
def get_NowGoal_AHOU(NowGoal_matchID, odds='both'):
    # odds = 'both'or'AH'or'OU'
    URL = 'http://data.nowgoal.com/oddscomp/'+str(NowGoal_matchID)+'.html'
    browser.get(URL)
    time.sleep(5)
    if odds=='both':
        AH = get_NowGoal_odds(NowGoal_matchID=URL, odds_Type='AH')
        OU = get_NowGoal_odds(NowGoal_matchID=URL, odds_Type='OU')
    elif odds=='AH':
        AH = get_NowGoal_odds(NowGoal_matchID=URL, odds_Type='AH')
        OU = None
    elif odds=='OU':
        AH = None
        OU = get_NowGoal_odds(NowGoal_matchID=URL, odds_Type='OU')
    else:
        'Please select either odds="both" or odds="AH" or odds="OU".'
    return AH,OU

# ===============================================================
def get_NowGoal_odds(NowGoal_matchID, odds_Type):
    if odds_Type == 'AH':
        odds = ('_AH', '_HM', '_AW')
        odds_attrs = {'id': 'Table1'}
        hover = ActionChains(browser).move_to_element(browser.find_element_by_id('card1'))
    if odds_Type == 'OU':
        odds = ('_OU', '_OV', '_UN')
        odds_attrs = {'id': 'Table2'}
        hover = ActionChains(browser).move_to_element(browser.find_element_by_id('card2'))
    #browser.refresh()
    hover.perform()
    content = browser.page_source
    soup = BeautifulSoup(''.join(content))
    table = soup.findAll('table', attrs = odds_attrs)[0]
    result = []
    for tabs in table:
        allrows = tabs.findAll('tr')
        for row in allrows:
            result.append([])
            allcols = row.findAll(text=True)[:-1] #take out last element
            for col in allcols:
                tab = col
                if tab == u'\xa0':
                    tab = tab.replace(u'\xa0',u'')
                    result[-1].extend(['',''])
                if u'\xa0 ' in tab:
                    tab = tab.replace(u'\xa0 ',u'')
                if 'showDate' in tab:
                    tab = tab[tab.index("(") + 1:tab.rindex(")")].replace('-1','').encode('utf8')
                    tab = [int(n) for n in tab.split(',')]
                    # GMT+0 = website default time - 8hours
                    tab = datetime(tab[0],tab[1],tab[2],tab[3],tab[4],tab[5])- timedelta(hours=8)
                    tab = tab.strftime('%d/%m/%Y %H:%M:%S')
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
    df = merge(df[[-1]], df[df.columns[:-1]], on = df.index, how = 'outer')
    #filter only AH/OU handicap column
    colname = df.filter(regex=odds[0]).columns
    for i in range(len(colname)):
        df1 = df[colname[i]].str.replace('/.*([\w.-]+)','')
        df1 = df1.str.replace('^-','').convert_objects(convert_numeric=True)
        df2 = df[colname[i]].str.replace('([\w.-]+).*/','')
        df2 = df2.str.replace('^-','').convert_objects(convert_numeric=True)
        symb = df[colname[i]].str.replace('[^-]','')
        symb = symb.str.replace('--','-')
        if all(df1)!='':
            sdf = abs((df1 + df2)/2)
        else:
            sdf = repeat('nan',len(df1))
        hdp = []
        for j in range(len(sdf)):
            hand = symb[j] + str(sdf[j])
            if hand == 'nan':
                hand = ''
            hdp.append(hand)
        df[colname[i]] = hdp
    #fill odds price in the blanks
    for i in range(1,len(df.columns)):
        for j in reversed(df.index[:-1]):
            if df[df.columns[i]][j] == '':
                df[df.columns[i]][j] = df[df.columns[i]][j+1]
            if df[df.columns[i]][j] is not '':
                df[df.columns[i]][j] = df[df.columns[i]][j]
    df = df.rename(columns = {'Update time':'Time_Updated'})
    df.Time_Updated = to_datetime(df.Time_Updated, dayfirst=True)
    return df[df.columns[1:]]

# ===============================================================
def create_mdb(path, filename):
    if not os.path.exists(path):
        os.makedirs(path)
    return pypyodbc.win_create_mdb(path + filename)

# ===============================================================
def saveMDB(path, dbase, filename, URL='7M', dataType='matches'):
    # URL = '7M' or 'NowGoal'; dataType = 'matches' or 'odds'
    # example 1:
    #    dbase = eng1112; filename = '201112'; dataType = 'matches'
    #    path = 'E:/Database/England/Eng_PR/'
    #    saveMDB(path, dbase, filename)
    # example 2:
    #    match = get_AHOU(eng1112.MatchID[6]) #rondomly select 6th element
    #                                           #as example
    #    dbase = match; filename = str(eng1112.MatchID[6]); dataType = 'odds'
    #    path = 'E:/Database/England/Eng_PR/'
    #    saveMDB(dbase, filename, dataType)
    # save data frame into excel xlsx format.
    dataType = dataType; URL = URL
    filename = str(filename)
    if dataType == 'matches':
        if not os.path.exists(path):
            os.makedirs(path)
        dbase.to_excel(path+filename+'.xlsx')
        # create a *.mdb database file if not exist.
        if not os.path.isfile(path+filename+'.mdb'):
            create_mdb(path, filename)
    elif dataType == 'odds':
        path_AH = path+'AH/'
        path_OU = path+'OU/'
        if not os.path.exists(path_AH):
            os.makedirs(path_AH)
        if not os.path.exists(path_OU):
            os.makedirs(path_OU)
        if URL == 'NowGoal':
            urlAHOU = 'http://data.nowgoal.com/oddscomp/'
            if urlAHOU not in dbase[0]:
                dbase[0].to_excel(path_AH+filename+'.xlsx')
                dbase[1].to_excel(path_OU+filename+'.xlsx')
        elif URL == '7M':
            # url_WDW = 'http://odds.7m.hk/en/1x2.shtml?id='
            url_AH = 'http://odds.7m.hk/en/odds.shtml?id='
            url_OU = 'http://odds.7m.hk/en/overunder.shtml?id='
            if url_AH not in dbase[0]:
                dbase[0].to_excel(path_AH+filename+'.xlsx')
            if url_OU not in dbase[1]:
                dbase[1].to_excel(path_OU+filename+'.xlsx')
        else:
            return 'Please choose either "7M" or "NowGoal" as URL.'
    else:
        return 'Please select dataType either "matches" or "odds".'
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
