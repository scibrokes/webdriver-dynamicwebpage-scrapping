library(rPython)
#'python.exec('from selenium import webdriver')
#'python.exec('browser = webdriver.Chrome()')
#'python.exec('browser.set_window_size(1015, 600)')
#'python.exec('browser.set_window_position(0, 200)')

#'python.load('C:/Users/Scibrokes Trading/Documents/GitHub/englianhu/WebDriver-DynamicWebpage-Scrapping/7M.py')
#'python.load('C:/Users/Scibrokes Trading/Documents/Github/englianhu/WebDriver-DynamicWebpage-Scrapping/NowGoal.py')
python.load('C:/Users/Scibrokes Trading/Documents/Github/englianhu/WebDriver-DynamicWebpage-Scrapping/Pymodel.py')
url0910 = 'http://data2.7m.cn/history_Matches_Data/2009-2010/92/en/index.shtml'
url1011 = 'http://data2.7m.cn/history_Matches_Data/2010-2011/92/en/index.shtml'
url1112 = 'http://data2.7m.cn/history_Matches_Data/2011-2012/92/en/index.shtml'
url1213 = 'http://data2.7m.cn/history_Matches_Data/2012-2013/92/en/index.shtml'

python.assign('url0910', url0910)
python.assign('url1011', url1011)
python.assign('url1112', url1112)

python.exec('eng0910 = get_7M_matches(url0910)')
python.exec('eng1011 = get_7M_matches(url1011)')
python.exec('eng1112 = get_7M_matches(url1112)')

eng0910 <- data.frame(python.get('eng0910'))
eng1011 <- data.frame(python.get('eng1011'))
eng1112 <- data.frame(python.get('eng1112'))
rm(url0910, url1011, url1112)

