from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(executable_path='/home/osama-laptop/chromedriver')


def one_team_with_date(date, team_id):
    driver.get("http://www.espn.com/nba/scoreboard/_/date/" + date)
    try:
        driver.find_element_by_xpath("html/body/div[@id='global-viewport']/section/section/div/section[@class='col-b']/div/div[@id='events']/article[@data-awayid='" + team_id + "']/div/section/a[@name='&lpos=nba:scoreboard:boxscore']").click()
    except:
        try:
            driver.find_element_by_xpath("html/body/div[@id='global-viewport']/section/section/div/section[@class='col-b']/div/div[@id='events']/article[@data-homeid='" + team_id + "']/div/section/a[@name='&lpos=nba:scoreboard:boxscore']").click()
        except:
            driver.close()
            return None
    time.sleep(5)
    game_id = driver.current_url[driver.current_url.find(('gameId=')) + 7:]
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup.prettify())
    box_score = {'gameId': int(game_id)}
    driver.close()
    return box_score

date = "20190221"
team_id = "5"
print(one_team_with_date(date, team_id))