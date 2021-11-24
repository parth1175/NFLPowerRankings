import time
import datetime
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# team rank / opponent rank to compare strength of schedule


def main():
    chrome_options = Options()
    chrome_options.headless = True # also works
    driver = webdriver.Chrome('/Users/landon/Downloads/chromedriver', options=chrome_options)  # Optional argument, if not specified will search path.

    passing_yards_url = 'https://www.teamrankings.com/nfl/stat/passing-yards-per-game'
    rankings_url = 'https://www.teamrankings.com/nfl/rankings/teams/'
    points_per_game_url = 'https://www.teamrankings.com/nfl/stat/points-per-game'
    interceptions_url = 'https://www.teamrankings.com/nfl/stat/interceptions-thrown-per-game'

    driver.get(rankings_url) # change this line of code based on feature needed
    sunday = get_prev_sunday()

    get_weekly_feature(driver, sunday, 'ranking') # change column's title and csv filename to 3rd parameter
    driver.quit()


def get_weekly_feature(driver, date, feature):
    feature = feature.replace(' ', '_')

    with open(f'{feature}.csv', 'w') as f:
        filewriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['year', 'month', 'day', 'team', f'{feature}'])

        selected_date = None
        while date.year > 2002:

            # change date until date-range is within football season
            while not (date.month >= 9 or date.month == 1 or date.month == 2):
                date = subtract_1_week(date)

            # change website's date to new date
            if selected_date is not None:
                if selected_date.year != date.year:
                    select_year(driver, date.year)
                if selected_date.month != date.month:
                    select_month(driver, date.month)
                # day always changes when selecting month/year
                select_day(driver, date.day)
            else:
                select_year(driver, date.year)
                select_month(driver, date.month)
                select_day(driver, date.day)

            selected_date = datetime.date(date.year, date.month, date.day)

            # only get ranks for in-season time range
            teams, features = get_feature(driver)
            for team, val in zip(teams, features):
                filewriter.writerow([str(date.year), str(date.month), str(date.day), team, val])
                print(str(date.year), str(date.month), str(date.day), team, val)

            date = subtract_1_week(date)


def get_feature(driver):
    search_box = driver.find_element(By.XPATH, "//table[@id='DataTables_Table_0']")
    table_body = search_box.find_element(By.XPATH, ".//tbody")
    table_rows = table_body.find_elements(By.XPATH, ".//tr")

    teams, features = [], []
    for row in table_rows:
        row_data = []
        for col in row.find_elements(By.XPATH, ".//td"):
            row_data.append(col.text)

        if len(row_data) >= 3:
            # if webscraping from /stat then 1st column is a rank column
            if row_data[0].isdigit():
                rank, team, feature, *other_cols = row_data
            # if webscraping from /rankings then 1st column is team name, not rank
            else:
                team, feature, *other_cols = row_data

            teams.append(team)
            features.append(feature)
        # print(f'{team}: {feature}')
    return teams, features


def select_year(driver, year):
    date = driver.find_element(By.XPATH, "//input[@class='custom-date']")
    date.click()
    time.sleep(0.25)  # allows date selection to open, creates visible html to access in code below

    date_picker_days = driver.find_element(By.XPATH, "//div[@class='datepicker-days']")
    date_picker_months = driver.find_element(By.XPATH, "//div[@class='datepicker-months']")
    date_picker_years = driver.find_element(By.XPATH, "//div[@class='datepicker-years']")

    days_table = date_picker_days.find_element(By.XPATH, ".//table")
    table_head = days_table.find_element(By.XPATH, ".//thead")
    table_head_date_selectors = table_head.find_elements(By.XPATH, ".//th")
    month_button = table_head_date_selectors[1]

    months_table = date_picker_months.find_element(By.XPATH, ".//table")
    table_head = months_table.find_element(By.XPATH, ".//thead")
    table_head_date_selectors = table_head.find_elements(By.XPATH, ".//th")
    year_button = table_head_date_selectors[1]

    years_table = date_picker_years.find_element(By.XPATH, ".//table")
    table_head = years_table.find_element(By.XPATH, ".//thead")
    table_head_date_selectors = table_head.find_elements(By.XPATH, ".//th")
    prev_decade_button = table_head_date_selectors[0]
    next_decade_button = table_head_date_selectors[2]

    month_button.click()
    time.sleep(0.25)

    year_button.click()
    time.sleep(0.25)

    table_body = years_table.find_element(By.XPATH, ".//tbody")
    table_rows = table_body.find_elements(By.XPATH, ".//tr")

    while True:
        for row in table_rows:
            cols = row.find_elements(By.XPATH, ".//span")
            for col in cols:
                if col.text == str(year):
                    col.click()
                    return
        prev_decade_button.click()


def select_month(driver, month):
    month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    date = driver.find_element(By.XPATH, "//input[@class='custom-date']")
    date.click()
    time.sleep(0.25)  # allows date selection to open, creates visible html to access in code below

    date_picker_days = driver.find_element(By.XPATH, "//div[@class='datepicker-days']")
    date_picker_months = driver.find_element(By.XPATH, "//div[@class='datepicker-months']")

    days_table = date_picker_days.find_element(By.XPATH, ".//table")
    table_head = days_table.find_element(By.XPATH, ".//thead")
    table_head_date_selectors = table_head.find_elements(By.XPATH, ".//th")
    month_button = table_head_date_selectors[1]

    months_table = date_picker_months.find_element(By.XPATH, ".//table")
    table_head = months_table.find_element(By.XPATH, ".//thead")
    table_head_date_selectors = table_head.find_elements(By.XPATH, ".//th")

    month_button.click()
    time.sleep(0.25)

    table_body = months_table.find_element(By.XPATH, ".//tbody")
    table_rows = table_body.find_elements(By.XPATH, ".//tr")

    for row in table_rows:
        cols = row.find_elements(By.XPATH, ".//span")
        for col in cols:
            if col.text == month_dict[month]:
                col.click()
                return


def select_day(driver, day):
    date = driver.find_element(By.XPATH, "//input[@class='custom-date']")
    date.click()
    time.sleep(0.25)  # allows date selection to open, creates visible html to access in code below

    date_picker_days = driver.find_element(By.XPATH, "//div[@class='datepicker-days']")

    days_table = date_picker_days.find_element(By.XPATH, ".//table")
    table_head = days_table.find_element(By.XPATH, ".//thead")
    table_head_date_selectors = table_head.find_elements(By.XPATH, ".//th")

    table_body = days_table.find_element(By.XPATH, ".//tbody")
    table_rows = table_body.find_elements(By.XPATH, ".//tr")

    for row in table_rows:
        cols = row.find_elements(By.XPATH, ".//td")
        for col in cols:
            if col.text == str(day):
                col.click()
                return


def get_prev_sunday():
    last_sunday = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday() + 1)
    return last_sunday


def subtract_1_week(date):
    return date - datetime.timedelta(days=7)


if __name__ == '__main__':
    main()

