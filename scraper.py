from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path='/home/osama-laptop/chromedriver')

date = "20190221"
sport = "nba"
team_id = "21"

driver.get("http://www.espn.com/" + sport + "/scoreboard/_/date/" + date)
driver.find_element_by_xpath("html/body/div[@id='global-viewport']/section/section/div/section[@class='col-b']/div/div[@id='events']/article[@data-awayid='" + team_id + "']").click()
