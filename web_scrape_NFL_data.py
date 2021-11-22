import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def main():
    chrome_options = Options()
    chrome_options.headless = True # also works
    driver = webdriver.Chrome('/Users/landon/Downloads/chromedriver', options=chrome_options)  # Optional argument, if not specified will search path.

    driver.get('https://www.teamrankings.com/nfl/rankings/teams/')
    get_ranks(driver)

    driver.quit()


def get_ranks(driver):
    search_box = driver.find_element(By.XPATH, "//table[@id='DataTables_Table_0']")
    table_body = search_box.find_element(By.XPATH, ".//tbody")
    table_rows = table_body.find_elements(By.XPATH, ".//tr")

    for row in table_rows:
        row_data = []
        for col in row.find_elements(By.XPATH, ".//td"):
            row_data.append(col.text)

        team, predictive_rank, home_rank, away_rank, last_5_rank, in_div_rank, strength_of_schedule = row_data
        print(f'{team}: {predictive_rank}')


if __name__ == '__main__':
    main()
