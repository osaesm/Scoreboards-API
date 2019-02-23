from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path='/home/osama-laptop/chromedriver')


def espn_nba_scraper(date, team_id):
    driver.get("http://www.espn.com/nba/scoreboard/_/date/" + date)
    try:
        driver.find_element_by_xpath("html/body/div[@id='global-viewport']/section/section/div/section[@class='col-b']/div/div[@id='events']/article[@data-awayid='" + team_id + "']/div/section/a[@name='&lpos=nba:scoreboard:boxscore']").click()
        return_val = "Found"
    except:
        try:
            driver.find_element_by_xpath("html/body/div[@id='global-viewport']/section/section/div/section[@class='col-b']/div/div[@id='events']/article[@data-homeid='" + team_id + "']/div/section/a[@name='&lpos=nba:scoreboard:boxscore']").click()
            return_val = "Found"
        except:
            return_val = None
    driver.close()
    return return_val

date = "20190221"
team_id = "5"
print(espn_nba_scraper(date, team_id))