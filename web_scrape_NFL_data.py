import time

from selenium import webdriver
from selenium.webdriver.common.by import By



driver = webdriver.Chrome('/Users/landon/Downloads/chromedriver')  # Optional argument, if not specified will search path.

driver.get('https://www.teamrankings.com/nfl/rankings/teams/')

search_box = driver.find_element(By.XPATH, "//table[@id='DataTables_Table_0']")
print(search_box)

time.sleep(3)
driver.quit()