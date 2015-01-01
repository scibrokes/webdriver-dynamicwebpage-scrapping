library(RSelenium)
lnk <- 'http://data2.7m.cn/history_Matches_Data/2009-2010/92/en/index.shtml'

remDr <- remoteDriver(browserName = "chrome")
#'remDr$setImplicitWaitTimeout(3000)
remDr$open()
remDr$navigate(lnk)

tableElem <- remDr$findElement("id", "e_run_tb")
xData <- tableElem$getElementAttribute("outerHTML")[[1]]
xData <- htmlParse(xData, encoding = "UTF-8")
mRnd <- readHTMLTable(xData)$e_run_tb
rm(tableElem, xData)

lapply(as.list(seq(nrow(mRnd))), function(i){
  lapply(as.list(seq(ncol(mRnd))), function(j){
    webElem <- remDr$findElement(using = 'xpath', paste0('//*[@id="e_run_tb"]/tbody/tr[',i,']/td[',j,']'))
    webElem$clickElement()

    tableElem <- remDr$findElement("id", "Match_Table")
    xData <- tableElem$getElementAttribute("outerHTML")[[1]]
    xData <- htmlParse(xData, encoding = "UTF-8")
    readHTMLTable(xData)})})


