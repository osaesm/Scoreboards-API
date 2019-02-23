from selenium import webdriver

driver = webdriver.Chrome(executable_path='/home/osama-laptop/chromedriver')

driver.get("http://www.espn.com/nba/scoreboard/_/date/20190209")
print("Title: " + driver.title)
elem = driver.find_element_by_id("401071501")
child_elements = elem.find_elements_by_xpath('.//*')

for child in child_elements:
    print(child.text)


driver.quit()
