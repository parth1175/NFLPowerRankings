import time
import datetime
from dateutil.relativedelta import *
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import multiprocessing
from multiprocessing import Pool, cpu_count


# team rank / opponent rank to compare strength of schedule


def main():
    chrome_options = Options()
    chrome_options.headless = True # also works
    driver = webdriver.Chrome('/Users/landon/Downloads/chromedriver', options=chrome_options)  # Optional argument, if not specified will search path.

    # overall
    scoring_margin_url = 'https://www.teamrankings.com/nfl/stat/average-scoring-margin'
    points_per_game_url = 'https://www.teamrankings.com/nfl/stat/points-per-game'

    # offensive
    #completion_percent_url = 'https://www.teamrankings.com/nfl/stat/completion-pct'
    ypg_url = 'https://www.teamrankings.com/nfl/stat/yards-per-game'
    #red_zone_TD_percent_url = 'https://www.teamrankings.com/nfl/stat/red-zone-scoring-pct'
    #offensive_ints_url = 'https://www.teamrankings.com/nfl/stat/interceptions-thrown-per-game'
    #third_down_conv_percent_url = 'https://www.teamrankings.com/nfl/stat/third-down-conversion-pct'
    #touchdowns_per_game_url = 'https://www.teamrankings.com/nfl/stat/touchdowns-per-game'
    yards_per_point_url = 'https://www.teamrankings.com/nfl/stat/yards-per-point'

    # defensive
    # opponent_ypg_url = 'https://www.teamrankings.com/nfl/stat/opponent-yards-per-game'
    # takeaways_url = 'https://www.teamrankings.com/nfl/stat/takeaways-per-game'
    # opponent_third_down_conv_url = 'https://www.teamrankings.com/nfl/stat/opponent-third-down-conversion-pct'
    # opponent_comp_percent_url = 'https://www.teamrankings.com/nfl/stat/opponent-completion-pct'
    # opponent_red_zone_comp_percent_url = 'https://www.teamrankings.com/nfl/stat/opponent-red-zone-scoring-pct'
    # sack_percent_url = 'https://www.teamrankings.com/nfl/stat/sack-pct'

    # master_schedule_url = 'https://www.pro-football-reference.com/years/2009/games.htm'
    driver.get(scoring_margin_url) # change this line of code based on feature needed

    sunday = get_prev_sunday()
    get_weekly_feature(driver, sunday, 'scoring margin', column=5) # change column's title and csv filename to 3rd parameter
    # get_master_schedule(driver)

    driver.quit()


def log_data():
    pass


def get_weekly_feature(driver, date, feature, column=3):
    feature = feature.replace(' ', '_')

    with open(f'{feature}.csv', 'a') as f:
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
            # if date.month == 9 and date.day == 12 and date.year == 2021:
            #     print('break')

            teams, features = get_feature(driver, column)

            for team, val in zip(teams, features):
                filewriter.writerow([str(date.year), str(date.month), str(date.day), team, val])
                print(str(date.year), str(date.month), str(date.day), team, val)

            date = subtract_1_week(date)


def get_feature(driver, column):
    search_box = driver.find_element(By.XPATH, "//table[@id='DataTables_Table_0']")
    table_body = search_box.find_element(By.XPATH, ".//tbody")
    table_rows = table_body.find_elements(By.XPATH, ".//tr")

    teams, features = [], []
    for row in table_rows:
        row_data = []
        for col in row.find_elements(By.XPATH, ".//td"):
            row_data.append(col.text)

        if len(row_data) >= column:
            # if webscraping from /stat then 1st column is a rank column
            if row_data[0].isdigit():
                rank, team, *other_cols = row_data
                feature = row_data[column-1]
            # if webscraping from /rankings then 1st column is team name, not rank
            else:
                team, *other_cols = row_data
                feature = row_data[column-1]

            # only include rows that aren't blank
            if team != '' and feature != '--':
                teams.append(team)
                features.append(feature)
        # print(f'{team}: {feature}')
    return teams, features


def get_master_schedule(driver, season=2021):

    with open(f'master_schedule.csv', 'a') as f:
        filewriter = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Date', 'Winner/tie', 'Loser/tie', 'PtsW', 'PtsL'])

        while season > 2002:
            search_box = driver.find_element(By.XPATH, "//table[@id='games']")
            table_body = search_box.find_element(By.XPATH, ".//tbody")
            table_rows = table_body.find_elements(By.XPATH, ".//tr")

            back_button = driver.find_element(By.XPATH, "//a[@class='button2 prev']")

            weekly_matchups = []
            for row in table_rows:
                row_data = []
                for col in row.find_elements(By.XPATH, ".//td"):
                    row_data.append(col.text)

                if len(row_data) >= 9:
                    day, date, time_str, team1, _, team2, _, team1_score, team2_score, *_ = row_data

                    if team1_score != '' and team2_score != '':
                        d = datetime.datetime.strptime(date, '%Y-%m-%d')
                        next_sunday = d + relativedelta(weekday=SU)
                        next_sunday = str(next_sunday.date())

                        weekly_data = [next_sunday, team1, team2, team1_score, team2_score]
                        weekly_matchups.append(weekly_data)

            back_button.click()
            time.sleep(0.25)
            season -= 1

            for d in weekly_matchups:
                filewriter.writerow([d[0], d[1], d[2], d[3], d[4]])
                print(d[0], d[1], d[2], d[3], d[4])


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


def get_next_sunday():
    last_sunday = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday() + 1)
    friday = datetime.date.today() + datetime.timedelta((6 - today.weekday()) % 7)

    return last_sunday


def subtract_1_week(date):
    return date - datetime.timedelta(days=7)


def lookup_name(name):
    dict = {"Baltimore": "Baltimore Ravens",
            "Buffalo": "Buffalo Bills",
            "New Orleans": "New Orleans Saints",
            "Pittsburgh": "Pittsburgh Steelers",
            "Seattle": "Seattle Seahawks",
            "New England": "New England Patriots",
            "NY Giants": "New York Giants",
            "Denver": "Denver Broncos",
            "Miami": "Miami Dolphins",
            "LA Rams": "Los Angeles Rams",
            "Tampa Bay": "Tampa Bay Buccaneers",
            "Tennessee": "Tennessee Titans",
            "Cincinnati": "Cincinnati Bengals",
            "Chicago": "Chicago Bears",
            "Washington": "Washington Football Team",
            "Jacksonville": "Jacksonville Jaguars",
            "Arizona": "Arizona Cardinals",
            "San Francisco": "San Francisco 49ers",
            "Philadelphia": "Philadelphia Eagles",
            "LA Chargers": "Los Angeles Chargers",
            "NY Jets": "New York Jets",
            "Houston": "Houston Texans",
            "Dallas": "Dallas Cowboys",
            "Indianapolis": "Indianapolis Colts",
            "Minnesota": "Minnesota Vikings",
            "Atlanta": "Atlanta Falcons",
            "Kansas City": "Kansas City Chiefs",
            "Cleveland": "Cleveland Browns",
            "Green Bay": "Green Bay Packers",
            "Carolina": "Carolina Panthers",
            "Las Vegas": "Las Vegas Raiders",
            "Detroit": "Detroit Lions"}


if __name__ == '__main__':
    main()



"""
df.rename(columns={"Winner/tie": "team", "Loser/tie": "opponent"})

flipped = df['column1','column2', 'column3', 'column5', 'column4', 'column6']

pd.concat([df1, df2])

data = pd.read_csv('./weeklyMatchups.csv')
roster = pd.Dataframe(data)
"""