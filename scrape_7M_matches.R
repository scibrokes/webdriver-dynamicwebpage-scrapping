library(rPython)
#'python.exec('browser = webdriver.Chrome()')
#'python.exec('browser.set_window_size(1015, 600)')
#'python.exec('browser.set_window_position(0, 200)')

#'python.load('C:/Users/Scibrokes Trading/Documents/Python Scripts/7M.py')
#'python.load('C:/Users/Scibrokes Trading/Documents/Python Scripts/NowGoal.py')
python.load('C:/Users/Scibrokes Trading/Documents/Python Scripts/Pymodel.py')
url0910 = 'http://data2.7m.cn/history_Matches_Data/2009-2010/92/en/index.shtml'
url1011 = 'http://data2.7m.cn/history_Matches_Data/2010-2011/92/en/index.shtml'
url1112 = 'http://data2.7m.cn/history_Matches_Data/2011-2012/92/en/index.shtml'
url1213 = 'http://data2.7m.cn/history_Matches_Data/2012-2013/92/en/index.shtml'

python.assign('url0910', url0910)
python.assign('url1011', url1011)
python.assign('url1112', url1112)

python.exec('get_7M_matches(url0910)')
python.exec('get_7M_matches(url1011)')
python.exec('get_7M_matches(url1112)')

